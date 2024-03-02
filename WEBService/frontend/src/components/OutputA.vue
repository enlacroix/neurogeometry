<template>
  <div class="tabs__wrapper">
    <div class="tabs">
      <div class="tab-header">
        <div class="disable"
             :class="{'active': isBaseActive || only_base}"
             @click="isBaseActive = true"
        >
          Наводки к решению
        </div>
        <div class="disable"
             :class="{'active': !isBaseActive && !only_base}"
             v-if="!only_base"
             @click="isBaseActive = false"
        >
          Подробное решение
        </div>
      </div>
      <div class="tab-indicator-background"></div>
      <div class="tab-indicator left-position-indicator"
           :class="{'right-position-indicator': !isBaseActive && !only_base,
            'full-position-indicator': only_base}"></div>
      <div class="tab-body">
        <div class="active">
          <div
              v-if="isBaseActive"
              v-html="answerText"
              class="output_window_field_base"
          >
          </div>
          <div
              v-if="!isBaseActive"
              v-html="answerFullText"
              class="output_window_field_base"
          >
            </div>
          <p></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "output-a",
  components: {},
  props: {
    only_base: {
      type: Boolean,
      default: true,
      required: true,
    },
    task_answer: {
      type: String,
      default: '',
      required: false,
    },
    task_answer_full: {
      type: String,
      default: '',
      required: false,
    }
  },
  data() {
    return {
      data_answer: '',
      isBaseActive: true,
    }
  },
  methods: {

  },
  computed: {
    answerText: function(){
      return this.$props.task_answer;
    },
    answerFullText: function(){
      return this.$props.task_answer_full;
    },
    },
}
</script>

<style lang="sass">

.tabs__wrapper
  padding-top: 90px
  max-height: 650px
  height: 70vh
  margin-bottom: 10px
  padding-bottom: 10px


.tabs
  color: rgb(146, 205, 232)
  width: 100%
  height: 65vh
  border-radius: 10px
  overflow: hidden


.tabs
  .tab-header
    background: #eef6ff
    height: 50px
    display: flex
    align-items: center
    justify-content: center


.tabs
  .tab-header
    div
      width: calc(100% / 2)
      text-align: center
      color: #3188C8
      font-weight: 500
      cursor: pointer
      font-size: 16px
      outline: none
      position: center

.tabs
  .tab-header
    div.active
      color: $main-color


.tabs
  .tab-indicator-background
    position: relative
    left: 0px
    width: 100%
    height: 3px
    background: rgba(45, 91, 183, 0.5)

.tabs
  .tab-indicator
    position: relative
    width: calc(100% / 2)
    height: 3px
    background: $main-color
    top: -3px
    border-radius: 5px
    transition: all 250ms ease-in-out

.tabs
  .tab-body
    position: relative
    height: calc(100% - 10px)


.tabs .tab-body > div
  position: relative
  padding-top: 2px
  height: 100%
  opacity: 0
  transform: scale(0.97)
  transition: opacity 500ms ease-in-out 0ms, transform 500ms ease-in-out 0ms


.tabs .tab-body > div.active
  height: 100%
  width: 100%
  top: -5px
  opacity: 1
  transform: scale(1)
  margin-top: 0px

.left-position-indicator
  left: 0px

.right-position-indicator
  left: calc(100% / 2) !important


.full-position-indicator
  width: 100% !important
  left: 0px !important


.output_window_field_base
  width: 100%
  height: 100%
  max-height: 350px
  min-height: 210px
  resize: none
  background: rgb(246, 251, 255)
  border-color: rgba(0, 0, 0, 0)
  padding: 10px
  font-size: 16px
  color: $main-color
  font-weight: 500
  overflow: auto

.output_window_field_base:focus
  border-color: rgba(0, 0, 0, 0)

</style>