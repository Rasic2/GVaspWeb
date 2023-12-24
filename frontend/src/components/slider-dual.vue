<!-- Use preprocessors via the lang attribute! e.g. <template lang="pug"> -->
<template>
  <div id="app">
    <div class="slider">
      <div class="slider-head">
        <div class="slider-name">
          <span class="slider-text">
            xlim
          </span>
        </div>
        <div class="slider-info">
          <input type="number" v-model.number="inputValue[0]" :min="min" :max="rangeMaxLower" :step="step"
            @blur="inputDone" @keyup.esc="inputCancel" @keyup.enter="inputDone" class="slider-input o-lower"
            :class="{ 'o-error': !validLower }" />
          <div class="slider-info-dual" v-if="isRange">
            <span class="slider-info-separator">~</span>
            <input type="number" v-model.number="inputValue[1]" :min="rangeMinUpper" :max="max" :step="step"
              @blur="inputDone" @keyup.esc="inputCancel" @keyup.enter="inputDone" class="slider-input o-upper"
              :class="{ 'o-error': !validUpper }" />
          </div>
        </div>
      </div>
      <div class="slider-range-wrapper" :style="styles" :class="{ 'o-range': isRange }">
        <input type="range" v-model.number="rangeValue[0]" :min="min" :max="max" :step="step" @input="emitRange"
          class="slider-range o-lower" />
        <input type="range" v-model.number="rangeValue[1]" :min="min" :max="max" :step="step" v-if="isRange"
          @input="emitRange" class="slider-range o-upper" />
      </div>
    </div>
  </div>
</template>
      
<script>
export default {
  data() {
    return {
      min: 0,
      max: 150,
      step: 0.1,
      value: [20, 50],
      rangeValue: [20, 50],
      inputValue: [20, 50]
    };
  },
  watch: {
    value: function () {
      this.rangeValue = [...this.formatValue];
      this.inputValue = [...this.formatValue];
    }
  },
  computed: {
    rangeMaxLower: function () {
      if (this.isRange) {
        return this.maxLower || this.rangeValue[1];
      } else {
        return this.max;
      }
    },
    rangeMinUpper: function () {
      if (this.isRange) {
        return this.minUpper || this.rangeValue[0];
      } else {
        return this.min;
      }
    },
    isRange: function () {
      return Array.isArray(this.value);
    },
    formatValue: function () {
      if (Array.isArray(this.value)) {
        return this.value;
      } else {
        return [this.value];
      }
    },
    validLower: function () {
      if (
        this.inputValue[0] >= this.min &&
        this.inputValue[0] <= this.rangeMaxLower
      ) {
        return true;
      } else {
        return false;
      }
    },
    validUpper: function () {
      if (this.isRange) {
        return (
          this.inputValue[1] >= this.rangeMinUpper &&
          this.inputValue[0] <= this.max
        );
      } else {
        // not range return true
        return true;
      }
    },
    styles: function () {
      const styles = {};
      let range = 0;
      if (this.isRange) {
        range = this.rangeValue[1] - this.rangeValue[0];
        const percent =
          ((this.rangeValue[0] - this.min) / (this.max - this.min)) * 100;
        styles["--left"] = `${Math.min(Math.max(percent, 0), 100)}%`;
      } else {
        range = this.rangeValue[0] - this.min;
      }
      const percent = (range / (this.max - this.min)) * 100;
      styles["--width"] = `${Math.min(Math.max(percent, 0), 100)}%`;
      return styles;
    }
  },
  methods: {
    isValid(value) {
      return value >= this.min && value <= this.max;
    },

    inputCancel() {
      this.inputValue = this.formatValue;
    },

    emitRange() {
      if (this.validLower && this.validUpper) {
        if (this.isRange) {
          this.value = this.rangeValue;
        } else {
          this.value = this.rangeValue[0];
        }
      } else {
        this.rangeValue = [...this.formatValue];
      }
    },

    inputDone() {
      if (this.validLower && this.validUpper) {
        if (this.isRange) {
          this.value = this.inputValue;
        } else {
          this.value = this.inputValue[0];
        }
      } else {
        this.inputValue = [...this.formatValue];
      }
    }
  }
};
</script>
      
<!-- Use preprocessors via the lang attribute! e.g. <style lang="scss"> -->
<style lang="scss">
$slider-bg: #e5e5e5;
$black-border: rgba(0, 0, 0, 0.15);
$black-divider: rgba(0, 0, 0, 0.1);
$primary: #1890ff;
$danger: #f5222d;
$white: #fff;

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.slider {
  position: relative;
  margin: 0 16px;
  padding: 12px 0;
  width: 320px;

  &-head {
    display: flex;
    justify-content: space-between;
  }

  &-name {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 14px;
    color: rgba(0, 0, 0, 0.65);

    .svg-icon {
      width: 16px;
      height: 16px;
      margin-right: 8px;
    }
  }

  &-input {
    width: 72px;
    height: 24px;
    border-radius: 4px;
    padding: 0 8px;
    border: 1px solid $black-border;
    font-size: 12px;

    &:hover,
    &:focus {
      border: 1px solid $primary;
      outline: none;
    }

    &.o-error {
      border: 1px solid $danger;
    }
  }

  &-info {
    display: flex;

    &-separator {
      margin: 0 4px;
    }
  }

  &-range {
    position: relative;
    -webkit-appearance: none;
    margin: 0;
    outline: none;
    border: none;
    width: 100%;
    top: 2px;
    height: 4px;
    background-color: transparent;
    z-index: 2;

    &::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 16px;
      height: 16px;
      box-sizing: border-box;
      border-radius: 50%;
      border: solid 2px $primary;
      background-color: $white;
      pointer-events: auto;
      cursor: pointer;
    }

    &.o-upper {
      position: absolute;
      top: 12px;
      left: 0;
      width: 100%;
    }

    &-wrapper {
      position: relative;
      height: 24px;

      &.o-range {
        input {
          pointer-events: none;
        }

        &::before {
          margin-left: var(--left);
        }
      }

      &::before {
        content: "";
        position: absolute;
        top: 12px;
        height: 4px;
        left: 0;
        width: var(--width);
        border-radius: 2px 0 0 2px;
        background-color: $primary;
        pointer-events: none;
        z-index: 1;
      }

      &::after {
        content: "";
        position: absolute;
        top: 12px;
        height: 4px;
        left: 0;
        right: 0;
        border-radius: 2px;
        background-color: $slider-bg;
        pointer-events: none;
      }
    }
  }
}
</style>