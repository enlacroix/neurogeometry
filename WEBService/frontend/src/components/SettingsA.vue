<template>
  <div class="dialog_header"><h3>Настройки модели</h3></div>
<div style="margin-top: 20px; margin-left: 20px; margin-bottom: 20px">

  <label class="checkbox_container">
    Бета
    <label class="settings_hint" data-tooltip="Открывает дополнительные опции (например, аддитивность отрезков),
     но возможна нестабильная работа прилоежния">?</label>
  <input type="checkbox" checked="checked" v-model="settings.beta">
  <span class="checkmark"></span>
</label>

  <label class="checkbox_container">
    Полное исследование
    <label class="settings_hint" data-tooltip="При нахождении ответа, продолжается исследование,
         так возможен поиск более красивого и изящного решения">?</label>
  <input type="checkbox" checked="checked" v-model="settings.is_full_searching">
  <span class="checkmark"></span>
</label>

  <label class="checkbox_container">
    Использовать метод линейных углов
    <label class="settings_hint" data-tooltip="
    Появляется специальное поле ввода (убедитесь, что вы ввели условие!).
    Вводимые данные объекты, заключённые в [ ], разделенные ';'.
    В них через ',' с пробелом перечисленны прямые, записанные в виде двух(!) заглавных букв">?</label>
  <input type="checkbox" checked="checked" v-model="settings.use_linear_angle_method">
  <span class="checkmark"></span>
</label>

  <div class="range_wrapper">
<div class="range_container">
  <div class="range_slider">
  <input type = "range" min="1" max="4"  v-model="settings.hints_amount"/>
    <div class="out_container">
    <span class="output_value minvalue">1</span>
	<output class="output_value"  :value="settings.hints_amount"></output>
      <span class="output_value maxvalue" >4 </span>
  </div>
  </div>
  <label class="range_label">Количество подсказок
    <label class="settings_hint" data-tooltip="Количество выдаваемых подсказок">?</label>
  </label>
  </div>
  </div>

  <div class="range_wrapper">
<div class="range_container">
  <div class="range_slider">
  <input type = "range" min="10" max="200"  v-model="settings.variables_limit"/>
    <div class="out_container">
    <span class="output_value minvalue">10 </span>
	<output class="output_value"  :value="settings.variables_limit"></output>
      <span class="output_value maxvalue" >200 </span>
  </div>
  </div>
  <label class="range_label">Лимит переменных
    <label class="settings_hint" data-tooltip="Количество переменных в одной задаче. Можно оптимизировать решение">?</label>
  </label>
  </div>
  </div>

    <div class="range_wrapper">
<div class="range_container">
  <div class="range_slider">
  <input type = "range" min="5" max="15"  v-model="settings.max_iter_amount"/>
    <div class="out_container">
    <span class="output_value minvalue">5</span>
	<output class="output_value" :value="settings.max_iter_amount"></output>
      <span class="output_value maxvalue" >15 </span>
  </div>
  </div>
  <label class="range_label">Максимальное количество итераций
  <label class="settings_hint" data-tooltip="Число итераций, через которое алгоитрм точно прекратит работать">?</label>
  </label>
  </div>
  </div>

  <button-a @click="give_settings" class="accept_settings">Принять</button-a>

</div>
</template>

<script>
export default {
  name: "settings-a",
  props: {
    settings_prop: {
      type: Object,
      default: {
        is_full_searching: false,
        variables_limit: 50,
        max_iter_amount: 10,
        use_linear_angle_method: false,
        beta: false,
        hints_amount: 2,
      },
      required: true,
    },
  },
  data() {
    return {
      settings: {
        is_full_searching: false,
        variables_limit: 50,
        max_iter_amount: 10,
        use_linear_angle_method: false,
        beta: false,
        hints_amount: 2,
      },
    }
  },
  methods: {
    give_settings() {
      this.$emit('give_settings', this.settings);
    }
  },
  beforeMount() {
    this.settings = this.settings_prop;
  }
}
</script>

<style lang="sass">
/////////////////////HINT/////////////////////////////
.settings_hint
  background-color: rgba(45, 91, 183, 0.8)
  border-radius: 20px
  min-width: 20px
  margin: auto
  text-align: center

[data-tooltip]
    position: relative /* Относительное позиционирование */

[data-tooltip]::after
    content: attr(data-tooltip) /* Выводим текст */
    position: absolute /* Абсолютное позиционирование */
    width: 300px /* Ширина подсказки */
    left: 0
    top: 0 /* Положение подсказки */
    background: rgba(45, 91, 183, 0.90) /* Синий цвет фона */
    color: #fff /* Цвет текста */
    padding: 0.5em /* Поля вокруг текста */
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3) /* Параметры тени */
    pointer-events: none /* Подсказка */
    opacity: 0 /* Подсказка невидима */
    transition: 1s /* Время появления подсказки */
    border-radius: 8px
    z-index: 500

[data-tooltip]:hover::after
    opacity: 1 /* Показываем подсказку */
    top: 2em /* Положение подсказки */


////////////////////////CHECKBOXES////////////////////////////////////
/* Customize the label (the container) */
.checkbox_container
  display: block
  position: relative
  padding-left: 35px
  margin-bottom: 12px
  cursor: pointer
  font-size: 20px
  -webkit-user-select: none
  -moz-user-select: none
  -ms-user-select: none
  user-select: none
  max-width: 560px


/* Hide the browser's default checkbox */
.checkbox_container input
  position: absolute
  opacity: 0
  cursor: pointer
  height: 0
  width: 0


/* Create a custom checkbox */
.checkmark
  position: absolute
  top: 5px
  left: 2px
  height: 20px
  width: 20px
  background-color: #eee


/* On mouse-over, add a grey background color */
.checkbox_container:hover input ~ .checkmark
  background-color: #ccc


/* When the checkbox is checked, add a blue background */
.checkbox_container input:checked ~ .checkmark
  background-color: $main-color


/* Create the checkmark/indicator (hidden when not checked) */
.checkmark:after
  content: ""
  position: absolute
  display: none


/* Show the checkmark when checked */
.checkbox_container input:checked ~ .checkmark:after
  display: block


/* Style the checkmark/indicator */
.checkbox_container .checkmark:after
  left: 9px
  top: 5px
  width: 5px
  height: 10px
  border: solid white
  border-width: 0 3px 3px 0
  -webkit-transform: rotate(45deg)
  -ms-transform: rotate(45deg)
  transform: rotate(45deg)



////////////////////////RANGE SLIDERS////////////////////////////////////

.range_wrapper
  display: flex
  align-items: flex-start
  justify-content: left


.range_container
  display: flex
  max-width: 700px
  min-width: 400px
  width: 70%
  max-height: 100px
  min-height: 50px

.range_slider
  width: 50%
  max-width: 300px
  min-width: 250px
  margin-top: 2%
  margin-left: 2px

input[type="range"]
  -webkit-appearance: none !important /*Needed to reset default slider styles */
  width: 100%
  height: 10px
  background:
    color: $blue
  border: 1px solid darken( $blue, 4%)
    radius: 10px
  margin-left: 0px
  transition: all 0.3s ease

  &:hover
    background-color: lighten( $blue, 5%)

  //&:active + #rangevalue /*Here to do something to the value while moving the slider */


input[type="range"]::-webkit-slider-thumb
  -webkit-appearance: none !important
  width: 12px
  height: 12px
  background:
    color: $main-color
  border:
    radius: 15px
  box-shadow: 0px 0px 3px darken( $main-color, 15%)
  transition: all 0.5s ease

  &:hover
    background:
      color: darken( $main-color, 10%)

  &:active
    box-shadow: 0px 0px 1px darken( $main-color, 15%)

.out_container
  display: flex

.output_value
  text-align: center
  font-size: 13px
  display: block
  margin: auto
  padding: 5px 0px
  width: 100%
  color:  $main-color

.minvalue
  text-align: left !important

.maxvalue
  text-align: right !important

.range_label
  margin-top: 2%
  margin-left: 20px
  font-size: 20px

.accept_settings
  position: center
  margin-top: 5%
  margin-left: 80%

</style>