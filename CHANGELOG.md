# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2026-10-16

Added:
- Data List and LIST: new "filter empty" node that removes every empty entry
  (`None`, empty STRING, empty LIST/DICT/SET, ...); `0` and `False` are kept.
  An optional boolean switch also treats a STRING consisting only of whitespace
  as empty.

Fixed:
- "save IMAGE to file" and "save IMAGE+MASK to file" no longer fail with
  "EXIF data is too long" when saving a JPG whose embedded workflow metadata is
  larger than a single JPEG EXIF block. A JPEG can only carry one 16-bit-sized
  EXIF segment, so oversized metadata is now reduced step by step - first the
  full workflow graph, then the workflow prompt info, then the prompt metadata -
  and the reduction is reported; the image itself is always written. Should
  embedding metadata ever fail for another reason, the image is written again
  without metadata instead of not at all.

## [2.1.0] - 2026-09-19

Backward compatible changes:
- "save IMAGE to file" and "save IMAGE+MASK to file" can now be used like
  ComfyUI's built-in "Save Image" node: images written into the output (or temp)
  folder are reported back to the frontend, so the node shows a preview of what
  it saved and the images appear in ComfyUI's generated-images list. In addition
  both nodes got a second `images` output that passes the images through
  unchanged, like the built-in node does.
- files written somewhere else (plain `path` mode) are still saved, they just
  cannot be previewed, as ComfyUI can only serve files from its own folders
- Both save nodes now embed ComfyUI's workflow metadata (the API prompt and the
  full workflow) in addition to the existing prompt metadata. Dragging a saved
  file back onto the canvas therefore restores the workflow, while the explicitly
  given `prompt` / `negative_prompt` remain in the `parameters` text that image
  viewers display and that is easy to extract afterwards. This is what makes the
  two channels worth having when a whole batch is saved from a data list: the
  workflow then contains every prompt of the graph, whereas `parameters` always
  holds the prompt of the image that was actually written.
- ComfyUI's `--disable-metadata` option suppresses both channels, exactly like
  it does for the built-in save node
- No widget was added, removed or reordered, so existing workflows keep their
  saved widget values.


## [2.0.0] - 2026-09-11

Critical change that ensures reliablity and **should** have no bad side 
effects, but when you see any, please report:
- DICT, LIST, SET and Data List nodes (plus the DICT/LIST-taking STRING nodes)
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
