import React, { useEffect, useState } from 'react';
import DATA from './services/datalist'
import { ReactSearchAutocomplete } from 'react-search-autocomplete'

const SearchPage = () => {

  const [query, setQuery] = useState('');
  const [results, setResults] = useState([0]);
  const [queryResults, setQueryResults] = useState([]);
  const handleSearch=(e)=>{
      e.preventDefault();
  }
  const items = [
      {
        id: 0,
        name: 'Cobol'
      },
      {
        id: 1,
        name: 'JavaScript'
      },
      {
        id: 2,
        name: 'Basic'
      },
      {
        id: 3,
        name: 'PHP'
      },
      {
        id: 4,
        name: 'Java'
      }
    ]
  
    const handleOnSearch = (string, results) => {
      // onSearch will have as the first callback parameter
      // the string searched and for the second the results.
      console.log(string, results)
    }
  
    const handleOnHover = (result) => {
      // the item hovered
      console.log(result)
    }
  
    const handleOnSelect = (item) => {
      // the item selected
      console.log(item)
    }
  
    const handleOnFocus = () => {
      console.log('Focused')
    }
  
    const formatResult = (item) => {
      return (
        <>
          <span style={{ display: 'block', textAlign: 'left' }}>id: {item.id}</span>
          <span style={{ display: 'block', textAlign: 'left' }}>name: {item.name}</span>
        </>
      )
    }

  useEffect ( () => {
    console.log("inside use effect")
    const getData = async () => {
      setQueryResults(await DATA.QueryData())
      console.log(queryResults)}
    getData();
  },[])

  return (
    <div className='SearchPageMain'>
    <div className='SearchPageResults'>
        <div className='SearchResults1'>
        {/* <form onSubmit={handleSearch}>
            <input type="text" value={query} onChange={e => setQuery(e.target.value)} />
            <button type="submit">Search</button>
        </form> */}
        <ReactSearchAutocomplete
                items={items}
                onSearch={handleOnSearch}
                onHover={handleOnHover}
                onSelect={handleOnSelect}
                onFocus={handleOnFocus}
                autoFocus
                formatResult={formatResult}
            />
            <br/>
        {results.length > 0 ? (
            // <ul>
            //   {results.map(result => (
            //     <li key={result.id}>
            //       <a href={result.url}>{result.title}</a>
            //       <p>{result.snippet}</p>
            //     </li>
            //   ))}
            // </ul>
            // <html>
            // <body>
            <div>
            <div className='reddit_embed'>
                <iframe
                    id="reddit-embed"
                    src="https://www.redditmedia.com//r/IndiaSpeaks/comments/zpre2v/2_judges_cant_decide_bjp_mps_strong_objection_on/j0uassz?limit=0/?ref\_source=embed\&amp;ref=share\&amp;embed=true&limit=5"
                    sandbox="allow-scripts allow-same-origin allow-popups"
                    style={{border: "none", overflow: "auto" }}
                    height="500"
                    width="1000"
                ></iframe>
            </div>
            <div className='reddit_embed'>
                <iframe
                    id="reddit-embed"
                    src="https://www.redditmedia.com//r/IndiaSpeaks/comments/zpre2v/2_judges_cant_decide_bjp_mps_strong_objection_on/j0uassz?limit=2/?ref\_source=embed\&amp;ref=share\&amp;embed=true&limit=5"
                    sandbox="allow-scripts allow-same-origin allow-popups"
                    style={{border: "none", overflow: "auto" }}
                    height="500"
                    width="1000"
                ></iframe>
            </div>
            </div>
            // </body>
            // </html>
            ) : (
            <p>No results found.</p>
        )}
        </div>
        <div className="side-box">
            <div>
                Top searched terms
            </div>
            <br/>
            <div className='buttons-start'>
            {items.map((object_ele,i)=>
            <button className='btn-orange' onClick={onclick} key={i}>{object_ele.name}</button>
            )}
            </div>
        </div>
    </div>
    </div>
  );
}

export default SearchPage;
