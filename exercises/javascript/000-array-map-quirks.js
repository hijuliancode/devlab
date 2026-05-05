
const tasks = [
  { name: 'Task A', priority: 1 },
  { name: 'Task B', priority: 2 },
  , // Hueco intencional
  { name: 'Task C', priority: 4 },
  { name: 'Task D', priority: 5 },
]

console.log("tasks", tasks)

console.log("Modificar una tarea que aún no fue visitada (para ver que sí refleja el cambio)")
tasks.map((task, idx) => {
  if (idx === 0) tasks[1].priority = 999
})
console.log('tasks',  tasks)

console.log("Eliminar otra antes de que sea visitada (para ver que se salta)")
tasks.map((task, idx) => {
  if (idx === 0) delete tasks[3]
})
console.log('tasks',  tasks)

console.log("Agregar una tarea nueva al final (para ver que no se visita)")
tasks.map((task, idx) => {
  if (idx === 0) tasks.push({ name: 'Hi, :)?', priority: 10 })
  console.log('task >', task)
})
console.log('tasks',  tasks)


console.log("Meter un hueco a propósito y verificar que no se procesa")

tasks.map((task, idx) => console.log(task.name, task.priority ** 2))
