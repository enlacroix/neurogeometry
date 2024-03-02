<template>
  <header-a
  @give_command="get_command"
  :settings_prop="settings"
  @give_settings="get_settings"
  />
  <main>
    <main-background/>
    <section class="main-sect">
      <div class="container">
        <div class="main__field">

          <div class="box input__task">
            <textarea type="text" class="input__field"
                      v-model="task_data.condition"
                      @change="clickCondition"
                      @click="clickCondition"
            ></textarea>
            <label class="input__label">Условие задачи</label>
          </div>

          <div class="box input__question" v-if="settings.use_linear_angle_method">
            <textarea type="text" class="input__field"
                      v-model="task_data.linear_angles"
            ></textarea>
            <label class="input__label">Линейные углы</label>
          </div>

          <div class="box input__question">
            <textarea type="text" class="input__field"
                      v-model="task_data.question"
                      @change="clickQuestion"
                      @click="clickQuestion"
            ></textarea>
            <label class="input__label">Вопрос задачи</label>
          </div>

          <div class="error_input" v-if="view.isError"><p>
              {{ task_data.error_message }}
            </p></div>
          <div class="error_input" v-if="view.isSyntaxError"><p v-html="task_data.syntax_error_message">
            </p></div>
          <div class="solve__button">
            <button-a @click="send_data">Решай</button-a>
          </div>

          <output-a
              :only_base="false"
              :task_answer="task_data.answer"
              :task_answer_full="task_data.answer_full"
          />

        </div>
      </div>
    </section>

    <div class="loader" :class="{'loading': view.isLoading}">
      <div class="spinner">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
  </main>
</template>

<script>
import HeaderA from "@/components/HeaderA";
import OutputA from "@/components/OutputA";
import MainBackground from "@/components/BackgroundA";
import axios from "axios";

export default {
  name: "MainPage",
  components: {HeaderA, MainBackground, OutputA},
  data() {
    return {
      task_data: {
        condition: '',
        question: '',
        linear_angles: '',
        answer: 'Введите условие и вопрос задачи чтобы получить решение',
        answer_full: 'Введите условие и вопрос задачи чтобы получить решение',

        last_is_condition: true,

        error_message: '',
        syntax_error_message: ''
      },

      settings: {
        is_full_searching: false,
        variables_limit: 50,
        max_iter_amount: 10,
        use_linear_angle_method: false,
        beta: false,
        hints_amount: 2,
      },

      view: {
        isLoading: false,
        isError: false,
        isSyntaxError: false,
      },
    }
  },
  methods: {
    identify_error(str_){
      if (str_ === 'MISSING_KEYS_IN_THE_REQUEST') {
        return 'Что-то пошло не так 😥 Попробуйте перезагрузить страничку.';
      } else if (str_ === 'EMPTY_CONDITION') {
        return 'Вы не ввели условие задачи(';
      } else if (str_ === 'SYNTAX_ERROR_IN_THE_CONDITION') {
        return 'Проверьте правильность заполнения поля условия';
      } else if (str_ === 'EMPTY_QUESTION') {
        return 'Вы не ввели вопрос задачи(';
      } else if (str_ === 'SYNTAX_ERROR_IN_THE_QUESTION') {
        return 'Проверьте правильность заполнения поля вопороса';
      } else if (str_ === 'EMPTY_LINEAR_ANGLES') {
        return 'Вы не ввели вопрос задачи с линейными углами(';
      } else if (str_ === 'SYNTAX_ERROR_IN_THE_LINEAR_ANGLES') {
        return 'Проверьте правильность заполнения поля для линейных углов';
      }
      return 'Что-то пошло не так 😥 Проверьте корректность введенного вами запроса или попробуйте перезагрузить страничку';
    },
    parse_syntax_error(obj_) {
      let str_ = 'Вы допустили синтаксическую ошибку в ';
      if (obj_['where'] === 'CONDITION') str_ += 'Условии. '
      else if (obj_['where'] === 'QUESTION') str_ += 'Вопросе. '
      else if (obj_['where'] === 'LINEAR_ANGLES') str_ += 'Линейных углах. '
      else str_ += '?. '
      str_ += '<br> Ошибка в команде: ' + obj_['command'] + '<br>'
      if (obj_['typeof'] === 'WRONG_AMOUNT_PARAMS') str_ += 'Неправильное число параметров. Должно быть: ' + obj_['correction'];
      else if (obj_['typeof'] === 'UNKNOWN_COMMAND') str_ += 'Неизвестная команда.'
      else if (obj_['typeof'] === 'LOST_BRACKET') str_ += 'Упущена скобка при написании команды'
      else if (obj_['typeof'] === 'WRONG_TYPE_PARAM') str_ += '"' + obj_['correction'] +  '" неподходящий тип параметра для команды'

      return str_
    },
    front_send_data() {
      this.view.isLoading = true;
      this.view.isError = false;
      this.view.isSyntaxError = false;
      this.task_data.error_message = '';
      this.task_data.answer = 'Введите условие и вопрос задачи чтобы получить решение';
      this.task_data.answer_full = 'Введите условие и вопрос задачи чтобы получить решение';
    },
    check_task_fields() {

      if (this.task_data.condition.length === 0) {
        this.task_data.error_message = this.identify_error('EMPTY_CONDITION');
        this.view.isError = true;
        this.view.isLoading = false;
        return false;
      }
      if (!this.settings.use_linear_angle_method) {
        this.task_data.linear_angles = '';
      }
      if (this.task_data.question.length === 0) {
        this.task_data.error_message = this.identify_error('EMPTY_QUESTION');
        this.view.isError = true;
        this.view.isLoading = false;
        return false;
      }
      if (this.task_data.linear_angles.length === 0 && this.settings.use_linear_angle_method) {
        this.task_data.error_message = this.identify_error('EMPTY_LINEAR_ANGLES');
        this.view.isError = true;
        this.view.isLoading = false;
        return false;
      }
      return true;
    },
    async send_data() {
      this.front_send_data();
      if (!this.check_task_fields()) return;

      const host_ = 'http://localhost:8000';
      //const host_ = 'https://neurogeometry.ru';

      await axios
          .post(
              host_ + '/v1/try/',
              {
                 task_data: {
                   condition: this.task_data.condition,
                   question: this.task_data.question,
                   linear_angles: this.task_data.linear_angles,
                 },
                settings:  this.settings,
              }
          )
          .then(({data}) => {
            console.log(data)
            this.task_data.answer = data.task_data.answer;
            this.task_data.answer_full = data.task_data.answer_full;
            this.view.isError = (data.task_data.error_message.length !== 0);
            this.task_data.error_message = '';
            if (this.view.isError) {
              this.task_data.error_message = this.identify_error(data.task_data.error_message);
              if (data.task_data.error_message === 'SYNTAX_ERROR_IN_THE_CONDITION' ||
                  data.task_data.error_message === 'SYNTAX_ERROR_IN_THE_QUESTION' ||
                  data.task_data.error_message === 'SYNTAX_ERROR_IN_THE_LINEAR_ANGLES') {
                this.view.isSyntaxError = true;
                this.task_data.syntax_error_message = this.parse_syntax_error(data.task_data.error_dict);
              }
            }
            console.log(this.task_data.error_message);
          })
          .catch(function (error) {
            console.log(error);
          });

      this.view.isLoading = false;
    },
    clickQuestion() {
      this.task_data.last_is_condition = false;
    },
    clickCondition() {
      this.task_data.last_is_condition = true;
    },
    get_command(command_) {
      let sep = '; ';
      let str_ = (this.task_data.last_is_condition ? this.task_data.condition : this.task_data.question);

      if (str_.length === 0) sep = '';
      else {
        for (let i = str_.length - 1; i >= 0; i -= 1) {
          if (str_[i] !== ' ' && str_[i] !== ';') break;
          if (str_[i] === ';') sep = ' ';
        }
      }

      str_ += sep + command_;

      if (this.task_data.last_is_condition) {
        this.task_data.condition = str_;
      } else {
        this.task_data.question = str_;
      }
    },
    get_settings(settings_) {
      this.settings = settings_;
    }
  }
}
</script>


<style lang="sass">

.main-sect
  height: 100vh
  max-height: 900px
  min-height: 684px
  position: relative

  .container
    padding-top: $header-height

.main
  &__field
    margin-left: auto
    margin-right: auto
    position: center
    padding-top: 20px

@media (min-width: 1100px)
  .main
    &__field
      width: 80%

@media (min-width: 1300px)
  .main
    &__field
      width: 65%

.box
  margin-top: 15px !important
  background: rgba(170, 210, 253, 0.2)
  backdrop-filter: blur(5px)
  border: 1px solid rgba(255, 255, 255, 0.18)
  vertical-align: center
  align-items: center
  justify-content: center
  border-radius: 10px

.input__task
  position: relative
  width: 100%
  padding: 1%
  display: flex
  flex-direction: column
  max-height: 140px
  min-height: 130px
  height: 100vh

.input__question
  position: relative
  width: 100%
  padding: 1%
  display: flex
  flex-direction: column
  max-height: 100px
  min-height: 80px
  height: 100vh

  .input__field:focus ~ label, textarea:valid ~ label
    transform: translateY(-160%) scale(0.9)

.input__field
  width: 100%
  height: 200%
  resize: none
  border: solid 20px #9e9e9e
  background: none
  padding-top: 1rem
  padding-left: 5px
  padding-right: 5px
  font-size: 17px
  color: $main-color
  transition: border 150ms cubic-bezier(0.4, 0, 0.2, 1)


.input__field:focus, textarea:valid
  outline: none
  border: 2px solid #264c96

.input__label
  position: absolute
  left: 15px
  color: $main-color
  pointer-events: none
  transform: translateY(1rem)
  transition: 150ms cubic-bezier(0.4, 0, 0.2, 1)


.input__field:focus ~ label, textarea:valid ~ label
  transform: translateY(-240%) scale(0.9)
  background-color: $main-color
  color: $main-color-2
  font-size: 16px
  font-weight: 500
  padding: 0 .2em


.error_input
  color: red
  margin: auto
  font-weight: 500
  font-size: 16px
  text-align: center
  padding-top: 10px


.solve__button
  padding-top: 15px
  float: right


////////SPINER////////
.loader
  top: 0
  bottom: 0
  right: 0
  left: 0
  display: none
  position: fixed
  width: 100vw
  height: 100vh
  z-index: 100000
  background: rgba(255, 255, 255, 0.1)
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.17)
  backdrop-filter: blur(11.5px)
  -webkit-backdrop-filter: blur(11.5px)
  animation: anim_opacity 500ms ease

.spinner
  scale: 300%
  position: relative
  top: 50%
  left: 50%


.loader.loading
  display: block


@keyframes anim_opacity
  0%
    opacity: 0
  100%
    opacity: 1

.spinner
  width: 44px
  height: 44px
  animation: spinner-y0fdc1 2s infinite ease
  transform-style: preserve-3d


.spinner > div
  background-color: rgba(0, 77, 255, 0.2)
  height: 100%
  position: absolute
  width: 100%
  border: 2px solid #004dff


.spinner div:nth-of-type(1)
  transform: translateZ(-22px) rotateY(180deg)


.spinner div:nth-of-type(2)
  transform: rotateY(-270deg) translateX(50%)
  transform-origin: top right


.spinner div:nth-of-type(3)
  transform: rotateY(270deg) translateX(-50%)
  transform-origin: center left


.spinner div:nth-of-type(4)
  transform: rotateX(90deg) translateY(-50%)
  transform-origin: top center

.spinner div:nth-of-type(5)
  transform: rotateX(-90deg) translateY(50%)
  transform-origin: bottom center


.spinner div:nth-of-type(6)
  transform: translateZ(22px)


@keyframes spinner-y0fdc1
  0%
    transform: rotate(45deg) rotateX(-25deg) rotateY(25deg)
  50%
    transform: rotate(45deg) rotateX(-385deg) rotateY(25deg)
  100%
    transform: rotate(45deg) rotateX(-385deg) rotateY(385deg)


</style>
