import { useQuery } from '@apollo/client/react'
import { GET_CHARACTERS } from '../graphql/queries'
import LoadingSpinner from './loading-spinner'
import ErrorComponent from './error-component'
import { useRef, useState } from 'react';

interface Character {
  id: string;
  name: string;
  status: string;
  species: string;
  image: string;
}

interface GetCharactersData {
  characters: {
    results: Character[]
  }
}

export default function Characters() {
  const [inputValue, setInputValue] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const { data, loading, error } = useQuery<GetCharactersData>(GET_CHARACTERS, {
    variables: { name: searchTerm }
  })

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorComponent /> 

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInputValue(value)

    if (debounceRef.current) {
      clearTimeout(debounceRef.current)
    }

    debounceRef.current = setTimeout(() => {
      setSearchTerm(value)
    }, 500);

  }

  return (
    <div>
      <input
        type="text"
        value={inputValue}
        onChange={handleChange}
        placeholder="Search character by name..."
        className="mb-6 w-full max-w-md rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-800 shadow-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
      />

      {data?.characters.results.map((character) => (
        <div key={character.id}>
          <img src={character.image} alt={character.name} />
          <h2>{character.name}</h2>
          <p>{character.status} - {character.species}</p>
        </div>
      ))}
    </div>
  )
}