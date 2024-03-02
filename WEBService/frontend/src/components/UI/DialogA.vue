<template>
  <div class="dialog" v-if="show" @click.stop="hideDialog">
    <div class="pv_close_btn"></div>
    <div @click.stop class="dialog_content">
      <div class="dialog_wrapper">
        <div class="dialog_wrapper_2">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "dialog-a",
  props: {
    show: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    hideDialog() {
      this.$emit("update:show", false)
    }
  }
}
</script>

<style lang="sass">
.dialog
  top: 0
  bottom: 0
  right: 0
  left: 0
  background: rgba(0, 0, 0, 0.6)
  position: fixed
  display: flex
  z-index: 999999


.dialog_content
  margin: auto
  background: rgb(204, 227, 255)
  opacity: 1
  width: 80%
  border-radius: 20px
  min-height: 220px
  //min-width: 400px
  padding: 20px
  max-height: 850px

@media (min-width: 1300px)
  .dialog_content
    width: 60%

@media (max-width: 850px)
  .dialog_content
    width: 90% !important
    height: 90% !important
  .dialog_wrapper_2
    //height: 100% !important
    height: 80vh

.pv_close_btn
  display: block
  background-image: url(@/assets/img/pv_layer_controls.png)
  width: 16px
  height: 16px
  position: fixed
  top: 12px
  right: 12px
  background-position: -3px 0
  opacity: .5
  -webkit-transition: opacity 100ms linear
  transition: opacity 100ms linear
  cursor: pointer

.dialog_wrapper
  outline: none
  border: 2px solid #264c96
  margin: -10px -10px -10px -10px

.dialog_wrapper_2
  padding: 5px 10px 5px 10px
  max-height: 800px
  overflow: auto

::-webkit-scrollbar
    width: 7px

/* Track */
::-webkit-scrollbar-track
  box-shadow: inset 0 0 5px grey
  border-radius: 10px


/* Handle */
::-webkit-scrollbar-thumb
  background: rgba(45, 91, 183, 0.5)
  border-radius: 10px


/* Handle on hover */
::-webkit-scrollbar-thumb:hover
  background: rgba(45, 91, 183, 0.7)



</style>