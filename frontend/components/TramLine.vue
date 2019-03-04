<template>
  <g>
    <path
      :d="getLinePath()"
      :fill="getColorForLine()"
    />
  </g>
</template>

<script>
  import mapper from '~/utility/Mapper'

  export default {
    props: {
      line: {
        required: true,
        type: String
      },
      direction: {
        required: true,
        type: String
      },
      stops: {
        required: true,
        type: Array
      }
    },
    methods: {
      getLinePath() {
        let path = '';

        // first move to start point
        const startPoint = mapper.getStop(this.stops[0]);
        path += `M ${startPoint.x} ${startPoint.y}`;

        return path;
      },
      getColorForLine() {
        return mapper.getColorForLine(this.line);
      }
    }
  }
</script>
