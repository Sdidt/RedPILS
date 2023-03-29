import React, { useEffect, useState } from 'react';
import Iframe from 'react-iframe-click';
import { ReactSearchAutocomplete } from 'react-search-autocomplete'
import DATA from './services/datalist'
import dummy_data from "./services/topics.json"

const SearchPage = () => {

  const [query, setQuery] = useState('');
  const [results, setResults] = useState(dummy_data);
  const [queryResults, setQueryResults] = useState([]);
  const [dataCheck, setDataCheck] = useState(0);
  const [divClicked, setDivClicked] = useState([])
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
  const dummy_results = [
    {
      id: 0,
      embed_link: "https://www.redditmedia.com//r/IndiaSpeaks/comments/zpre2v/2_judges_cant_decide_bjp_mps_strong_objection_on/j0uassz?limit=2/?ref\_source=embed\&amp;ref=share\&amp;embed=true&limit=5"
    },
    {
      id: 1,
      embed_link: "https://www.redditmedia.com//r/IndiaSpeaks/comments/zpre2v/2_judges_cant_decide_bjp_mps_strong_objection_on/j0uassz?limit=2/?ref\_source=embed\&amp;ref=share\&amp;embed=true&limit=5"
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

  const handleIframeClick = (event) => {
    console.log(event)
    setDivClicked(result =>
      results.map((item, buttonIndex) => (buttonIndex === event ? true : item)));
    console.log(divClicked)
  }

  useEffect (() => {
    console.log("inside use effect")
    const getData = async () => {
      const dummy_data_store = await DATA.QueryData()
      console.log(dummy_data_store)
      setQueryResults(dummy_data_store)
      console.log(queryResults)
      setResults(dummy_results)
    }
    if(queryResults.length==0){
      getData();
    }
  },[dataCheck])
  console.log(queryResults)
  console.log(results)

  return (
    <div className='SearchPageMain'>
    <div className='SearchPageResults'>
        <div className='SearchResults1'>
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
        <div>
          {console.log(results.length)}
          {results.map((result,index) => 
            <div className='reddit_embed' key={result.id}>
                {/* <iframe
                    id={result.id}
                    src={result.embed_link}
                    sandbox="allow-scripts allow-same-origin allow-popups"
                    style={{border: "none", overflow: "auto" }}
                    height="500"
                    width="1000"
                ></iframe> */}
                <Iframe
                  // onInferredClick={() => console.log('You clicked')}
                  onInferredClick={() => handleIframeClick(index)}
                  // id={`iframe-${index}-${result.id}`}
                  id = {result.id}
                  src={result.embed_link}
                  sandbox="allow-scripts allow-same-origin allow-popups"
                  style={{border: "none", overflow: "auto" }}
                  height="500"
                  width="1000"
                ></Iframe>;
            </div>
            )}
        </div>
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
