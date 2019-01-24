class ConnectionStopMapper {
    constructor() {
        this.map = {};
    }

    getLineIndexForStop(stopId, lineName) {
        if (Object.keys(this.map).indexOf(`${stopId}`) > -1) {
            const listOfLines = this.map[stopId];
            const lineIndex = listOfLines.indexOf(lineName);
            if (lineIndex > -1) {
                return lineIndex;
            } else {
                this.map[stopId].push(lineName);
                return this.map[stopId].length - 1;
            }
        } else {
            this.map[stopId] = [lineName];
            return 0;
        }
    }

}

const _connectionStopMapper = new ConnectionStopMapper();
export default _connectionStopMapper;
