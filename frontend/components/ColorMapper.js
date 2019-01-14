const colors = [
    '#839496',
    '#93a1a1',
    '#b58900',
    '#cb4b16',
    '#dc322f',
    '#d33682',
    '#6c71c4',
    '#268bd2',
    '#2aa198',
    '#859900'
];

class ColorMapper {
    
    constructor() {
        this.colorMap = {};
    }

    getColorForLine(line) {
        const keys = Object.keys(this.colorMap);

        if (keys.indexOf(line) === -1) {
            this.colorMap[line] = colors[keys.length % colors.length];
        }

        return this.colorMap[line];
    }
}

const _colorMapper = new ColorMapper();
export default _colorMapper;