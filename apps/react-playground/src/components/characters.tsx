import { useQuery } from '@apollo/client/react'
import { GET_CHARACTERS } from '../graphql/queries'
import LoadingSpinner from './loading-spinner'
import ErrorComponent from './error-component'

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
  const { data, loading, error } = useQuery<GetCharactersData>(GET_CHARACTERS)

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorComponent /> 

  return (
    <div>

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