
# Kirby Remix Icons Plugin

A Kirby CMS plugin for easy integration of [Remix Icons](https://remixicon.com/). This plugin provides SVG icons for use in blueprints and the panel.

## Acknowledgments
Icons from [Remix Design](https://remixicon.com/). Support them at [BuyMeACoffee](https://buymeacoffee.com/remixdesign).

## Installation
1. Copy `kirby-remix-icons` to `/site/plugins/`.
2. Use icons in your blueprints by their names.

### Example Blueprint
```yaml
fields:
  fireLine:
    label: Fire Line Icon
    icon: fire-line
  fireFill:
    label: Fire Fill Icon
    icon: fire-fill
```

### Blueprint Examples
- **Fill Icon**: `arrow-down-box-fill`
- **Line Icon**: `arrow-down-line`

## Generate Your Icon Set
Use the Python script to include your own SVGs.

1. Organize SVGs in `icons/` with subfolders (optional).
2. Run the script:
   ```bash
   python3 generate_icons.py
   ```
3. Place the plugin in `/site/plugins/`.

### Example Icon Structure
```
icons/
    Arrows/
        arrow-down-box-fill.svg
        arrow-up-box-fill.svg
    Shapes/
        square-fill.svg
```

## License
Icons by [Remix Design](https://remixicon.com/). Check their site for terms.
