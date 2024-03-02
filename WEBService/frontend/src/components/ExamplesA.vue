<template>
  <div class="dialog_header"><h3>Примеры написания запроса</h3></div>
  <p class="dialog_info"> Наш сервис умеет на отлично решать задачи по Геометрии, но, к сожалению пока не умеет
    распознавать человеческий язык. Чтобы давать задачу нашему алгоритму мы придумали предикатный язык. Он достаточно
    прост в освоении и понимании. <br>
    Ниже мы собрали несколько примеров написания условия задач на предикатном языке. <br>
    Если вас интересует, что значит каждая команда, тыкнете на <span @click="switchToHelp" class="switch-span">Cправку</span>.
  </p>

  <div class="dialog_header"><h4>Задача 1. ЕГЭ 2018, Центр</h4></div>
  <p class="dialog_info"> Дан четырехугольник <i>ABCD</i>.
    Докажите, что отрезки <i>LN</i> и <i>KM</i>, соединяющие середины его противоположных сторон, делят друг друга попалам.
  </p>
  <span class="type-predicate-field"> Условие задачи: <br></span>
  <div class="predicate_view"> <p>
    Quadrangle(A, B, C, D);   mdp(M, A, D);   mdp(K, B, C);   mdp(H, D, C);  mdp(P, A, B);  mdp(F, P, H);   Line(M, F, K)
  </p></div>
  <span class="type-predicate-field"> Вопрос задачи: <br></span>
  <div class="predicate_view"> <p>
    mdp(F, M, K)
  </p></div>

  <div class="dialog_header"><h4>Задача 2. Геометрия 7-9, Атанасян, Бутузов</h4></div>
  <p class="dialog_info"> Дан треугольник <i>ABC</i>. Проведена прямая <i>MB</i>. Угол <i>BAC</i> = 20 градусов,
    <i>MBC</i> = 60 градусов, угол <i>ACB</i> в три раза больше чем угол <i>A</i>. Доказать, что <i>AC</i> параллельно <i>MB</i>.
  </p>
  <span class="type-predicate-field"> Условие задачи: <br></span>
  <div class="predicate_view"> <p>
    Triangle(A, B, C); Line(M, B); SetValue(Angle(B, A, C), 20); SetValue(Angle(M, B, C), 60); Relation(Angle(A, C, B), Angle(B, A, C), 3)
  </p></div>
  <span class="type-predicate-field"> Вопрос задачи: <br></span>
  <div class="predicate_view"> <p>
    prl(A, C, M, B)
  </p></div>

  <div class="dialog_header"><h4>Задача 3. ОГЭ, Тренировочные варианты</h4></div>
  <p class="dialog_info"> Дан прямоугольный треугольник <i>ABC</i> с гипотенузой <i>AB</i>. К ней была проведена медиана <i>CM</i>,
     а <i>E</i> - середина катета <i>BC</i>. Доказать, что <i>ME</i> перпендикулярен стороне <i>BC</i>.
  </p>
  <span class="type-predicate-field"> Условие задачи: <br></span>
  <div class="predicate_view"> <p>
    Triangle(A, B, C); ort(A, C, C, B); mdp(M, A, B); Line(C, M); Line(E, C, B); Line(M, E); mdp(E, C, B)
  </p></div>
  <span class="type-predicate-field"> Вопрос задачи: <br></span>
  <div class="predicate_view"> <p>
    ort(M, E, B, C)
  </p></div>

   <div class="dialog_header"><h4>Задача 4. Авторское</h4></div>
  <p class="dialog_info"> Дан треугольник <i>ABC</i> с периметром равным 12. <i>AM</i> = 4, <i>AM/AB</i> = 2.
    <i>M</i> - середина стороны <i>AC</i>. Доказать, что <i>BM</i> перпендикулярен стороне <i>AC</i>.
  </p>
  <span class="type-predicate-field"> Условие задачи: <br></span>
  <div class="predicate_view"> <p>
    Triangle(A, B, C); SetValue(Line(A, M), 4); Relation(Line(A, M), Line(A, B), 2); Sum((Line(A, B), Line(A, C), Line(B, C)), 12); mdp(M, A, C)
  </p></div>
  <span class="type-predicate-field"> Вопрос задачи: <br></span>
  <div class="predicate_view"> <p>
    ort(B, M, A, C)
  </p></div>

</template>

<script>
export default {
  name: "examples-a",
  props: {
  },
  data() {
    return {
    }
  },
  methods: {
    switchToHelp() {
      console.log('switchToHelp');
      this.$emit('switchToHelp', false);
    }
  }
}
</script>

<style lang="sass">

.switch-span
  color: $main-color
  font-weight: 500
  font-size: 17px
  cursor: pointer

.type-predicate-field
  font-weight: 600

.predicate_view
  padding: 5px 5px 5px 5px
  background-color: rgba(45, 91, 183, 0.2)
  font-size: 18px
  color: #1e347b
  font-weight: 500
  max-width: 900px
  border-radius: 7px
  margin-bottom: 10px
  p
    margin: auto


</style>