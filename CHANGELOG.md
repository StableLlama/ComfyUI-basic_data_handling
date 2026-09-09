# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Add "create DICT from JSON string" and "create LIST from JSON string" nodes to
  parse a multiline JSON object/array into a DICT/LIST
- "save IMAGE to file" and "save IMAGE+MASK to file": `format` is now a dropdown
  (still connectable as a STRING) whose entries are derived from the formats the
  installed Pillow/image plugins can actually write (RGB node offers them all,
  IMAGE+MASK only alpha-capable ones); every batch frame is written instead of
  only the first; and `path` can be switched to ComfyUI-style `filename_prefix`
  mode via a toggle, resolved through ComfyUI's own folder/file helpers
  (auto-numbered under the output dir); both modes accept ComfyUI templates such
  as `%date:yyyy-MM-dd%`

## [1.8.1] - 2026-09-06

- Add optional additional input for image saving to also save the prompt when provided
- Enhance in line documentation

## [1.8.0] - 2026-08-31

- Time delta nodes can now be converted to seconds (float) and milliseconds (int)

## [1.7.0] - 2026-08-27

- String save node now supports append mode
