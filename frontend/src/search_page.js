import React, { useState } from 'react';

const SearchPage = () => {

    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const handleSearch=(e)=>{
        e.preventDefault();
    }
  return (
    <div>
      <h1>My Search Engine</h1>
      <form onSubmit={handleSearch}>
        <input type="text" value={query} onChange={e => setQuery(e.target.value)} />
        <button type="submit">Search</button>
      </form>
      {results.length > 0 ? (
        <ul>
          {results.map(result => (
            <li key={result.id}>
              <a href={result.url}>{result.title}</a>
              <p>{result.snippet}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
}

export default SearchPage;
