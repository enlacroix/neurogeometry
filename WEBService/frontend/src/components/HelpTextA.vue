<template>
  <div class="dialog_header"><h4>Несколько важных правил и подсказок</h4></div>
  <p class="dialog_info">
    1) Команды разделяются знаком точка с запятой - ";" <br>
    2) Аргументы в команде, указываемые в крглых скобках, разделяются между собой запятными - "," <br>
    3) Условие и вопрос задачи пишуться в разных полях. <br>
    4) Перед переводом условия в предикатный вид нарисуйте или представьте черетеж к задаче у себя в голове. Так будет легче составлять правильный запрос.
  </p>
  <div class="dialog_header"> <h3>Сущности</h3> </div>
  <p class="dialog_info"> Точка - атомарная единица программы, сущности - следующая ступень абстракции, которая
    оборачивает их в прямые, отрезки, углы, отношения. <br>
    Другие сущности: </p>
  <div class="command_list">
    <p class="list_item"><b class="bold_com" @click="give_command('Line(X, Y, . . .)')">Line(X, Y, . . .)</b> - Прямая, содержащая точки X, Y и т.д. Аргументы Line лежат на одной прямой в строго
      определённом порядке. </p>
    <p class="list_item"><b class="bold_com" @click="give_command('Angle(A, B, C)')">Angle(A, B, C)</b> - Угол ∠ABC. </p>
    <p class="list_item"><b class="bold_com" @click="give_command('Ratio(A, B, C, D)')">Ratio(A, B, C, D)</b> - Отношение длин отрезков AB/CD. </p>
    <p class="list_item"><b class="bold_com" @click="give_command('LinAngle.quick(A, B, C, D)')">LinAngle.quick(A, B, C, D)</b> - Линейный угол ∠[AB, CD]. </p>
  </div>
  <div class="dialog_header"> <h3>Предикаты</h3> </div>
  <p class="dialog_info"> Некая функция от точек, которая показывает истинность геометрического утверждения, заложенного
    в предикате. <br>
    Знак многоточия - <b>. . .</b> , показывает, что на его месте может стоять произвольное количество точек. <br>
    Предикаты классифицируются с точки зрения способов проверки истинности. </p>

  <div class="dialog_header"> <h3>Свободные предикаты</h3> </div>
  <div class="command_list">
    <p class="list_item"><b class="bold_com" @click="give_command('cyl(  )')">cyl(. . .) </b> - <i>{cyclic}</i> Точки лежат на одной окружности.</p>
    <p class="list_item"><b class="bold_com" @click="give_command('_col_(  )')">_col_(. . .)</b> - <i>{collinear}</i> точки-аргументы лежат на одной прямой. Применять только в том случае, если <b>неизвестен</b>
      порядок точек! В остальных используй Line.
    </p>
  </div>
  <div class="dialog_header"> <h3>Фиксированные предикаты</h3> </div>
  <div class="command_list">
    <p class="list_item"><b class="bold_com" @click="give_command('mdp(M, A, B)')">mdp(M, A, B)</b> - <i>{midpoint}</i> точка M - середина отрезка АВ.</p>
    <p class="list_item"><b class="bold_com" @click="give_command('cir(X, A, B, C)')">cir(X, A, B, C)</b> - <i>{circle}</i> X - центр окружности, на которой лежат точки А, В и С.</p>
    <p class="list_item"><b class="bold_com" @click="give_command('citer(O, A, B, C)')">citer(O, A, B, C)</b> -  <i>{circumcenter}</i> O - центр описанной окружности треугольника АВС. </p>
    <p class="list_item"><b class="bold_com" @click="give_command('inter(I, A, B, C)')">inter(I, A, B, C)</b> - <i>{incenter}</i> O - центр вписанной окружности треугольника АВС.  </p>
  </div>

  <div class="dialog_header"> <h3>Квадропредикаты</h3> </div>
  <div class="command_list">
    <p class="list_item"><b class="bold_com" @click="give_command('prl(A, B, C, D)')">prl(A, B, C, D)</b> - <i>{parallel}</i> AB параллелен CD.</p>
    <p class="list_item"><b class="bold_com" @click="give_command('eql(A, B, C, D)')">eql(A, B, C, D)</b> - <i>{equal}</i> AB = CD.</p>
    <p class="list_item"><b class="bold_com" @click="give_command('ort(A, B, C, D)')">ort(A, B, C, D)</b> - <i>{orthogonal}</i> AB перпендикулярен (ортогонален) CD.</p>
    <p class="dialog_info">Их сущностные обобщения: </p>
    <p class="list_item"><b class="bold_com" @click="give_command('ORT(l1, l2)')">ORT(l1, l2)</b> - Прямые l1, l2 перпендикулярны друг другу.</p>
    <p class="list_item"><b class="bold_com" @click="give_command('PRL(l1, l2)')">PRL(l1, l2)</b> - Прямые l1, l2 параллельны друг другу.</p>
    <p class="list_item"><b class="bold_com" @click="give_command('ELA(a1, a2)')">ELA(a1, a2)</b> - <i>{Equal Linear Angles}</i> Линейные углы а1 и а2 равны.  </p>
  </div>
  <div class="dialog_header"> <h3>Сущностные предикаты</h3> </div>
  <div class="command_list">
    <p class="list_item"><b class="bold_com" @click="give_command('eqa(A, B, C, D, P, Q)')">eqa(A, B, C, D, P, Q)</b> - <i>{equal angles}</i> ∠[ABC] = ∠[DPQ], равенство углов.</p>
    <p class="list_item"><b class="bold_com" @click="give_command('etr(A, B, C, D, P, Q)')">etr(A, B, C, D, P, Q)</b> - <i>{equal triangles}</i> равные треугольники ABC и DPQ.</p>
    <p class="list_item"><b class="bold_com" @click="give_command('ctr(A, B, C, D, P, Q)')">ctr(A, B, C, D, P, Q)</b> - <i>{congruent triangles}</i> подобные треугольники ABC и DPQ.</p>
    <p class="list_item"><b class="bold_com" @click="give_command('eqr(A, B, C, D, P, Q, H, F)')">eqr(A, B, C, D, P, Q, H, F)</b> - <i>{equal ratios}</i> отношения длин отрезков АВ/СD = PQ/HF.</p>
  </div>
  <div class="dialog_header"> <h3>Функторы</h3> </div>
  <p class="dialog_info">x, y - обозначим так отрезки, углы или отношения. </p>
  <div class="command_list">
    <p class="list_item"><b class="bold_com" @click="give_command('Relation(x, y, k)')">Relation(x, y, k)</b> - x/y = k</p>
    <p class="list_item"><b class="bold_com" @click="give_command('LinearCombination({x: a1}, {y: a2}, ...)')">LinearCombination({x: a1}, {y: a2}, ...)</b> - линейная комбинация переменных с коэффициентами а1, а2 в сумме
      даст 0.
    </p>
    <p class="list_item"><b class="bold_com" @click="give_command('SetValue(x, val)')">SetValue(x, val)</b> - x = val.</p>
    <p class="list_item"><b class="bold_com" @click="give_command('Sum((args), result)')">Sum((args, . . .): list, result: int)')</b> - сумма величин в списке args равна числу result.</p>
  </div>
  <div class="dialog_header"> <h3>Фигуры и конструкции</h3> </div>
  <div class="command_list">
    <!--:smiling_imp: !БЕТА! :imp:-->
    <p class="dialog_info"> К каждому имени необходимо п.pointConstructor() </p>
    <p class="list_item">
      <b class="bold_com" @click="give_command('IsoTriangle')">IsoTriangle</b>
      <b> / </b>
      <b class="bold_com" @click="give_command('OrtTriangle')">OrtTriangle</b>
      <b> / </b>
      <b class="bold_com" @click="give_command('DescribedTriangle')">DescribedTriangle</b> - равнобедренный / прямоугольный / треугольник.
      Треугольник, в который вписана окружность. Их комбинации.
    </p>
    <p class="list_item">
      <b class="bold_com" @click="give_command('Circle')">Circle</b>
      <b> / </b>
      <b class="bold_com" @click="give_command('InscribedCircle')">InscribedCircle</b> - окружность, вписанная окружность.</p>
    <p class="list_item"><b class="bold_com" @click="give_command('Bisect')">Bisect</b> - биссектриса.</p>
  </div>
</template>

<script>
export default {
  name: "help-text-a",
  methods: {
    give_command(str_) {
      this.$emit('give_command', str_);
    },
  },
}
</script>

<style lang="sass">

.dialog_header
  font-size: 20px
  padding-left: 3%
  font-weight: bold
  color: #13254d
  line-height: 1.375
  margin-bottom: 0.25em
  border-bottom: 1px solid #3c5ea8
  max-width: 50%

.dialog_info
  font-size: 16px

.command_list
  //white-space: nowrap
  font-size: 15px
  flex-wrap: wrap
  .list_item
    text-indent: 20px
    .bold_com
      background-color: rgba(90, 126, 204, 0.62)
      border-radius: 5px
      font-size: 16px


</style>