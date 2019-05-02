<template>
  <path
    :d="path"
    fill="none"
    stroke="#3bbbd7"
    stroke-width="200"
  />
</template>

<script>
  export default {
    props: {
      minX: {
        required: true,
        type: Number
      },
      minY: {
        required: true,
        type: Number
      },
      maxY: {
        required: true,
        type: Number
      },
    },
    data() {
      return {
        // coordinates are in GK4 / Pulkovo 1942 Zone 4 format
        // converted with https://twcc.fr/
        coordinates: [
          [4632554, 5652165], // [50.984103, 13.885928],
          [4631740, 5653928], // [51.000132, 13.874981],
          [4630976, 5654984], // [51.009792, 13.864488],
          [4629762, 5655856], // [51.017902, 13.847519],
          [4629186, 5657291], // [51.030926, 13.839812],
          [4627845, 5658268], // [51.040002, 13.821056],
          [4626714, 5660376], // [51.059192, 13.805677],
          [4625125, 5660905], // [51.064293, 13.783205],
          [4623773, 5660586], // [51.061719, 13.763813],
          [4622572, 5659748], // [51.054449, 13.746414],
          [4621841, 5659957], // [51.056481, 13.736066],
          [4620516, 5662051], // [51.075571, 13.717864],
          [4619889, 5662126], // [51.076375, 13.708954],
          [4619424, 5661801], // [51.073553, 13.702204],
          [4619150, 5660908], // [51.065588, 13.698015],
          [4618019, 5660706], // [51.064002, 13.681815],
          [4616553, 5663563], // [51.089973, 13.661827],
          [4613789, 5664906]  // [51.102591, 13.622825]
        ]
      }
    },
    computed: {
      path() {
        let path = 'M ' + this.modifyXCoordinate(this.coordinates[0][0]) + ' ' + this.modifyYCoordinate(this.coordinates[0][1]);
        this.coordinates.forEach(e => path += ` L ${this.modifyXCoordinate(e[0])} ${this.modifyYCoordinate(e[1])}`);
        return path;
      }
    },
    methods: {
      modifyXCoordinate(x) {
        return x - this.minX;
      },
      modifyYCoordinate(y) {
        return (((y - this.minY) - (this.maxY - this.minY)) * -1) + 700;
      }
    }
  };
</script>
