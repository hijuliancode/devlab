import Characters from "./components/characters"

function App() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-3 p-8 w-full">
      <h1 className="text-4xl font-semibold tracking-tight text-gray-900 dark:text-gray-100">
        React Playground
      </h1>
      <p className="text-sm text-gray-500 dark:text-gray-400">
      </p>
      <Characters />
    </main>
  )
}

export default App
