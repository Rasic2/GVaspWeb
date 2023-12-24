<template>
  <div class="cat-input" :class="{ 'cat-input--suffix': showSuffix }">
    <!-- type：先判断是否有传入显示密码，控制输入框类型是文本/密码，然后是type传入的值 -->
    <input :type="showPassword ? (passwordVisiable ? 'text' : 'password') : type" class="cat-input__inner"
      :placeholder="placeholder" :name="name" :disabled="disabled" :class="{ 'is-disabled': disabled }" :value="value"
      @input="handleinput" />
    <span class="cat-input__suffix" v-if="showSuffix">
      <i class="cat-input__icon cat-icon-circle-close" v-if="clearable && value" @click="clear"></i>
      <i class="cat-input__icon cat-icon-view" :class="{ 'cat-icon-view-active': passwordVisiable }" v-if="showPassword"
        @click="handlepwd"></i>
    </span>
  </div>
</template>
   
<script>
export default {
  name: "CatInput",
  props: {
    placeholder: {
      type: String,
      default: "",
    },
    type: {
      type: String,
      default: "text",
    },
    name: {
      type: String,
      default: "",
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    value: {
      type: String,
      default: "",
    },
    clearable: {
      type: Boolean,
      default: false,
    },
    showPassword: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      passwordVisiable: false, //控制是否显示密码
    };
  },
  methods: {
    handleinput(event) {
      //父组件在绑定v-model时，其实就绑定的input事件，因此父组件不需要再声明事件了
      this.$emit("input", event.target.value);
    },
    clear() {
      this.$emit("input", "");
    },
    handlepwd() {
      this.passwordVisiable = !this.passwordVisiable;
    },
  },
  computed: {
    //有清空/显示密码，添加类名、显示span
    showSuffix() {
      return this.clearable || this.showPassword;
    },
  },
};
</script>