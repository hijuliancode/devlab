export default function ErrorComponent() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="rounded-lg shadow-md p-8 text-center">
        {/* Error icon */}
        <div className="w-16 h-16 mx-auto mb-4 bg-red-100 rounded-full flex items-center justify-center">
          <svg
            className="w-8 h-8 text-red-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </div>

        {/* Error message */}
        <h2 className="text-xl font-bold text-slate-100 mb-2">
          Something went wrong
        </h2>
        <p className="text-slate-300 mb-6">
          Failed to load the data. Please try again.
        </p>

        {/* Action button */}
        <button
          onClick={() => window.location.reload()}
          className="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded transition-colors"
        >
          Try Again
        </button>
      </div>
    </div>
  )
}
