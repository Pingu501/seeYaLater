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
    this.sideMapping = {};

    this.colorMap = {};
  }

  addStop = stop => this.stops[stop.id] = stop;

  getStop = stopId => this.stops[stopId];

  getOffsetForSide = (stopId, sideIndex) => {
    const keys = Object.keys(this.sideMapping);

    if (keys.indexOf(stopId) === -1) {
      this.sideMapping[stopId] = {1: 0, 2: 0, 3: 0, 4: 0};
    }

    this.sideMapping[stopId][sideIndex]++;
    return this.sideMapping[stopId][sideIndex];
  };

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
