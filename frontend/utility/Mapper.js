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


function getSide(previousStop, currentStop) {
  if (!previousStop) {
    return 2;
  }

  const dx = currentStop.x - previousStop.x;
  const dy = currentStop.y - previousStop.y;

  return Math.abs(dx) < Math.abs(dy) ? 1 : 2;
}

class Mapper {

  constructor() {
    this.stops = {};
    this.sideMapping = {};

    this.colorMap = {};
  }

  addStop = stop => this.stops[stop.id] = stop;

  getStop = stopId => this.stops[stopId];

  // get correct side of the stop, 1 is up, 2 is right, 3 is down, 4 is left
  getSideOfStop(previousStop, currentStop, line) {
    if (!this.sideMapping[currentStop.id]) {
      this.sideMapping[currentStop.id] = {};
    }

    if (!this.sideMapping[currentStop.id][line]) {
      const side = getSide(previousStop, currentStop);

      this.sideMapping[currentStop.id][line] = {
        side: side,
        offset: this.getOffsetForSide(currentStop, side)
      }
    }

    return this.sideMapping[currentStop.id][line];
  }

  getOffsetForSide(stop, side) {
    let offset = 0;
    Object.values(this.sideMapping[stop.id]).forEach(entry => {
      if (entry.side === side) {
        offset++;
      }
    });
    return offset;
  }

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
