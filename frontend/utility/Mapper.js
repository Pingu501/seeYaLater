const colors = [
  '#b58900',
  '#cb4b16',
  '#dc322f',
  '#d33682',
  '#6c71c4',
  '#268bd2',
  '#2aa198',
  '#859900'
];

class Mapper {

  constructor() {
    this.stops = {};
    this.colorMap = {};
  }

  addStop = stop => this.stops[stop.id] = stop;

  getStop = stopId => this.stops[stopId];

  getColorForLine(line) {
    const keys = Object.keys(this.colorMap);

    if (keys.indexOf(line) === -1) {
      this.colorMap[line] = colors[keys.length % colors.length];
    }

    return this.colorMap[line];
  }
}

const _mapper = new Mapper();
export default _mapper;
