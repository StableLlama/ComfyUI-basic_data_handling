# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-09-11

Critical change that ensures reliablity and **should** have no bad side 
effects, but when you see any, please report:
-  DICT, LIST, SET and Data List nodes (plus the DICT/LIST-taking STRING nodes)
  now degrade gracefully when their data source is not connected (`None`) instead
  of raising: read/query nodes return their natural "no data" result (the `get`
  default, an empty list, `False`, `0`, `None`), and transform nodes behave as if
  given an empty container.
- "save IMAGE to file" and "save IMAGE+MASK to file": `format` is now a dropdown
  (still connectable as a STRING) whose entries are derived from the formats the
  installed Pillow/image plugins can actually write (RGB node offers them all,
  IMAGE+MASK only alpha-capable ones); every batch frame is written instead of
  only the first; and `path` can be switched to ComfyUI-style `filename_prefix`
  mode via a toggle, resolved through ComfyUI's own folder/file helpers
  (auto-numbered under the output dir); both modes accept ComfyUI templates such
  as `%date:yyyy-MM-dd%`

Backward compatible changes:
  - Add a "continue if not empty" flow-control node: it passes a value through
  unchanged when it is non-empty, and blocks execution (via an execution blocker)
  when the value is empty. It is list-aware (`INPUT_IS_LIST` / `OUTPUT_IS_LIST`),
  so it is immune to ComfyUI's empty-input batching crash and passes data lists
  through unchanged. By default the block is silent; an optional `message` can be
  set to show a dialog. Use it before nodes that cannot handle an empty input
  (e.g. a node receiving an empty Data List) to stop execution instead of failing.
- Add "create DICT from JSON string" and "create LIST from JSON string" nodes to
  parse a multiline JSON object/array into a DICT/LIST


## [1.8.1] - 2026-09-06

- Add optional additional input for image saving to also save the prompt when provided
- Enhance in line documentation

## [1.8.0] - 2026-08-31

- Time delta nodes can now be converted to seconds (float) and milliseconds (int)

## [1.7.0] - 2026-08-27

- String save node now supports append mode
