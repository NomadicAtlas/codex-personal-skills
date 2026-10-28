#!/usr/bin/env python3
"""Generate a visibly marked draft/content-review poster, never a print release."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path
from importlib.metadata import version

from _common import (CliError, checked_output_file, commit_temp_file, emit_json,
                     finite_number, load_json_file, private_temp_file,
                     reject_unknown_keys, require_string, resolve_local_asset, sha256_file)
from _pptx import (analyze_layout, patch_accessibility_metadata, require_safe_pptx,
                   strip_generated_printer_settings)
from inventory_images import _read_image


def _font_checks(elements: list[dict]) -> list[dict]:
    """Report local family/glyph availability; never mistake fallback for a match."""
    reports = []
    for family in sorted({e['font_face'] for e in elements if e['type'] == 'text'}):
        record = {'requested_family': family, 'status': 'unverified'}
        if shutil.which('fc-match'):
            try:
                result = subprocess.run(['fc-match', '--format=%{family}\n%{file}', family],
                                        capture_output=True, text=True, timeout=5, check=True)
                actual, _, font_path = result.stdout.partition('\n')
                record.update(resolved_family=actual, resolved_file=font_path)
                record['status'] = ('family_available' if family.casefold() in
                    {x.strip().casefold() for x in actual.split(',')} else 'substituted')
                try:
                    from fontTools.ttLib import TTFont
                    with TTFont(font_path, fontNumber=0) as font:
                        cmap = font.getBestCmap() or {}
                        text = ''.join(e['text'] for e in elements
                                       if e['type'] == 'text' and e['font_face'] == family)
                        missing = sorted({c for c in text if not c.isspace() and ord(c) not in cmap})
                        record['missing_characters_in_resolved_font'] = ''.join(missing)
                        if missing:
                            record['status'] = 'missing_glyphs'
                except (ImportError, OSError, ValueError):
                    record['glyph_coverage'] = 'unverified'
            except (subprocess.SubprocessError, OSError):
                record['status'] = 'unverified'
        reports.append(record)
    return reports


def generate_review_poster(manifest: str, output: str, *, stage: str = 'draft') -> dict:
    if stage not in {'draft', 'content-final'}:
        raise CliError('stage must be draft or content-final')
    path, doc = load_json_file(manifest)
    reject_unknown_keys(doc, context='review poster', allowed={
        'schema_version', 'title', 'width_in', 'height_in', 'language',
        'elements', 'pending_content', 'pending_production', 'reviewed_by'},
        required={'schema_version', 'title', 'width_in', 'height_in', 'language',
                  'elements', 'pending_content', 'pending_production', 'reviewed_by'})
    if doc['schema_version'] != 'review-1.0':
        raise CliError('schema_version must be review-1.0')
    title = require_string(doc['title'], context='title', maximum=500)
    language = require_string(doc['language'], context='language', maximum=35)
    if not re.fullmatch(r'[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*', language):
        raise CliError('language must be a BCP 47-style tag')
    width = finite_number(doc['width_in'], context='width_in', minimum=1, maximum=56)
    height = finite_number(doc['height_in'], context='height_in', minimum=2, maximum=56)
    for key in ('pending_content', 'pending_production'):
        if not isinstance(doc[key], list) or len(doc[key]) > 100:
            raise CliError(f'{key} must be a bounded list')
        for item in doc[key]:
            require_string(item, context=key, maximum=1000)
    if doc['reviewed_by'] is not None:
        require_string(doc['reviewed_by'], context='reviewed_by', maximum=500)
    if stage == 'content-final' and (doc['pending_content'] or not doc['reviewed_by']):
        raise CliError('content-final requires no pending content and an actual reviewer')
    elements = doc['elements']
    if not isinstance(elements, list) or not 1 <= len(elements) <= 200:
        raise CliError('elements must contain 1–200 objects; first must be title text')
    pending = list(doc['pending_content'])
    prepared = []
    for i, item in enumerate(elements):
        common = {'type', 'x_in', 'y_in', 'width_in', 'height_in', 'source'}
        kind = item.get('type') if isinstance(item, dict) else None
        extra = {'text', 'font_face', 'font_size_pt', 'bold'} if kind == 'text' else {'path', 'sha256', 'alt_text'}
        if kind not in {'text', 'image'}:
            raise CliError(f'elements[{i}].type must be text or image')
        reject_unknown_keys(item, context=f'elements[{i}]', allowed=common | extra, required=common | extra)
        x, y, w, h = [finite_number(item[k], context=k, minimum=0 if k in {'x_in','y_in'} else .01, maximum=56)
                      for k in ('x_in','y_in','width_in','height_in')]
        if x+w > width+1e-6 or y+h > height-.45+1e-6:
            raise CliError(f'element {i} crosses canvas or reserved status footer')
        if item['source'] is None:
            pending.append(f'Element {i+1}: source requires confirmation')
        else:
            require_string(item['source'], context='source', maximum=2000)
        metadata = None
        if kind == 'text':
            require_string(item['text'], context='text', maximum=20000)
            require_string(item['font_face'], context='font_face', maximum=100)
            finite_number(item['font_size_pt'], context='font_size_pt', minimum=8, maximum=300)
            if type(item['bold']) is not bool:
                raise CliError('bold must be boolean')
        else:
            asset = resolve_local_asset(path.resolve(), item['path'], suffixes={'.png','.jpg','.jpeg'})
            if item['sha256'] != sha256_file(asset):
                raise CliError(f'element {i}: image hash mismatch')
            require_string(item['alt_text'], context='alt_text', maximum=2000)
            metadata = _read_image(asset)
            suspicious = [k for k in metadata['metadata_keys'] if any(t in k.lower() for t in
                          ('comment','description','exif','iptc','photoshop','software','xmp','xml'))]
            if metadata['exif_entry_count'] or metadata['embedded_text_keys'] or suspicious:
                raise CliError('image metadata requires local review/removal before embedding')
            item = dict(item, path=str(asset))
        prepared.append((item, metadata))
    if elements[0]['type'] != 'text' or elements[0]['text'] != title:
        raise CliError('first element must be text matching title exactly')
    if stage == 'content-final' and pending:
        raise CliError('content-final requires source confirmation for every element')

    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor
        from pptx.enum.text import MSO_AUTO_SIZE
    except ImportError as exc:
        raise CliError('review generation needs python-pptx and Pillow in the selected runtime') from exc
    destination = checked_output_file(output, suffix='.pptx')
    temps = []
    try:
        for _ in range(3):
            fd, tmp = private_temp_file(destination, suffix='.pptx')
            os.close(fd); temps.append(tmp)
        presentation = Presentation()
        presentation.slide_width, presentation.slide_height = Inches(width), Inches(height)
        slide = presentation.slides.add_slide(presentation.slide_layouts[5])
        presentation.core_properties.title = title
        presentation.core_properties.subject = f'{stage}; NOT PRINT-READY'
        presentation.core_properties.language = language
        alt = {}
        image_dpi = []
        for i, (item, metadata) in enumerate(prepared):
            x,y,w,h = (float(item[k]) for k in ('x_in','y_in','width_in','height_in'))
            if item['type'] == 'image':
                fit = min(w/metadata['width_px'],h/metadata['height_px'])
                pw,ph = metadata['width_px']*fit,metadata['height_px']*fit
                shape = slide.shapes.add_picture(item['path'],Inches(x+(w-pw)/2),Inches(y+(h-ph)/2),Inches(pw),Inches(ph))
                alt_name = f'R{i+1:03d}_IMAGE'
                alt[alt_name] = item['alt_text']
                shape.name = alt_name
                image_dpi.append({'element': i+1, 'effective_dpi_at_canvas_size': 1/fit})
            else:
                shape = slide.shapes.title if i == 0 else slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
                shape.left,shape.top,shape.width,shape.height = map(Inches,(x,y,w,h))
                shape.name = f'R{i+1:03d}_TEXT'
                tf = shape.text_frame; tf.text = item['text']; tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.NONE
                for paragraph in tf.paragraphs:
                    for run in paragraph.runs:
                        run.font.name = item['font_face']; run.font.size = Pt(item['font_size_pt']); run.font.bold = item['bold']
        footer = slide.shapes.add_textbox(0, Inches(height-.4), Inches(width), Inches(.35))
        footer.name = 'R999_STATUS'
        footer.text_frame.margin_top = footer.text_frame.margin_bottom = 0
        footer.text_frame.margin_left = footer.text_frame.margin_right = 0
        footer.text_frame.text = ('DRAFT — NOT FOR SUBMISSION OR PRINT' if stage == 'draft' else 'CONTENT REVIEWED — PRINT CHECKS PENDING')
        for run in footer.text_frame.paragraphs[0].runs:
            run.font.size = Pt(18); run.font.bold = True; run.font.color.rgb = RGBColor(160,0,0)
        presentation.save(temps[0])
        strip_generated_printer_settings(temps[0],temps[1])
        require_safe_pptx(temps[1])
        patch_accessibility_metadata(temps[1],temps[2],alt_text_by_shape_name=alt,language=language)
        package = require_safe_pptx(temps[2])
        layout = analyze_layout(temps[2],print_scale=1,minimum_font_pt_final=8)
        commit_temp_file(temps[2],destination)
    finally:
        for tmp in temps:
            tmp.unlink(missing_ok=True)
    return {'stage':stage,'print_ready':False,'output':str(destination),'sha256':sha256_file(destination),
            'input_sha256':sha256_file(path),'reviewed_by':doc['reviewed_by'],
            'pending_content':pending,'pending_production':doc['pending_production'],
            'package_safe':package['safe'],'layout':layout,'images':image_dpi,
            'font_checks':_font_checks(elements),
            'dependencies':{k:version(k) for k in ('python-pptx','Pillow','lxml')},
            'manual_checks_required':['Rendered fonts, glyphs, overflow, and layout',
                                      'Content and source accuracy', 'Final conference/printer requirements']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest')
    parser.add_argument('--output',required=True)
    parser.add_argument('--stage',choices=['draft','content-final'],default='draft')
    parser.add_argument('--report')
    args = parser.parse_args()
    try:
        if args.report:
            checked_output_file(args.report,suffix='.json')
        emit_json(generate_review_poster(args.manifest,args.output,stage=args.stage),output=args.report)
    except (CliError, OSError) as exc:
        parser.exit(2,f'error: {exc}\n')

if __name__ == '__main__':
    main()
