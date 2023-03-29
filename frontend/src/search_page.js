import React, { useEffect, useState } from 'react';
import Iframe from 'react-iframe-click';
import { ReactSearchAutocomplete } from 'react-search-autocomplete'
import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';
import Markup from 'react-html-markup';
import DATA from './services/datalist'
import dummy_data from "./services/topics.json"
import ProfilePictureCopy from "./pic1.png";

const SearchPage = () => {

  const [query, setQuery] = useState('');
  const [results, setResults] = useState(dummy_data);
  const [queryResults, setQueryResults] = useState([]);
  const [dataCollect, setDataCollect] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [divClicked, setDivClicked] = useState([])
  const handleSearch=(e)=>{
      e.preventDefault();
  }
  const items = [
      {
        id: 0,
        name: 'BJP'
      },
      {
        id: 1,
        name: 'Congress'
      },
      {
        id: 2,
        name: 'AAP'
      },
      {
        id: 3,
        name: 'Kejriwal'
      },
      {
        id: 4,
        name: 'Bla'
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

  const timeDropDown = [
    'All', '6h', '12h','24h','1d'
  ];
  const timeDropDownDefault = timeDropDown[0];

  const redditPolarityDropDown = [
    'All', '+ve', '-ve'
  ];
  const redditPolarityDefault = redditPolarityDropDown[0];
  
  const handleOnSearch = async(string, results) => {
    // onSearch will have as the first callback parameter
    // the string searched and for the second the results.
    if(string!=''){
      setSearchTerm(string)
    }
  }

  const handleOnHover = (result) => {
    // the item hovered
    // console.log(result)
  }

  const handleOnSelect = (item) => {
    // the item selected
    // console.log(item)
  }

  const handleOnFocus = () => {
    // console.log('Focused')
  }

  const handleButtonSearch = async(searchTerm) => {
    console.log(searchTerm)
    if(searchTerm!=""){
      const dummy_data_store = await DATA.QueryData(searchTerm)
      console.log(dummy_data_store['topk'])
      setDataCollect(dummy_data_store['topk'])
    }
    // else{
    //   const dummy_data_store = await DATA.QueryData('BJP')
    //   console.log(dummy_data_store['topk'])
    //   setDataCollect(dummy_data_store['topk'])
    // }
  }

  const handleKeywordSearch = async(searchTerm) => {
    console.log(searchTerm)
    const dummy_data_store = await DATA.QueryData(searchTerm)
    console.log(dummy_data_store['topk'].length)
    if(dummy_data_store['topk'].length==0){
      const dummy_data_store = await DATA.QueryData('BJP')
    }
    console.log(dummy_data_store['topk'])
    setDataCollect(dummy_data_store['topk'])
  }

  const formatResult = (item) => {
    return (
      <>
        {/* <span style={{ display: 'block', textAlign: 'left' }}>id: {item.id}</span>
        <span style={{ display: 'block', textAlign: 'left' }}>name: {item.name}</span> */}
        <span style={{ display: 'block', textAlign: 'left' }}>{item.name}</span>
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
      const dummy_data_store = await DATA.QueryData('BJP')
      console.log(dummy_data_store['topk'])
      setDataCollect(dummy_data_store['topk'])
      console.log(queryResults)
      setResults(dummy_results)
    }
    // if(queryResults.length==0){
    //   getData();
    // }
  },[dataCollect])
  console.log(queryResults)
  console.log(results)

  return (
    <div className='SearchPageMain'>
    <div className='SearchPageResults'>
        <div className='SearchResults1'>
          <div className='SearchBarDiv'>
            <div className='SearchBar'>
            <ReactSearchAutocomplete
                items={items}
                onSearch={handleOnSearch}
                onHover={handleOnHover}
                onSelect={handleOnSelect}
                onFocus={handleOnFocus}
                autoFocus
                showIcon={true}
                placeholder="Search"
                formatResult={formatResult}
                styling={{borderRadius: "8px"}}
            />
            </div>
            <div className='dropdowndiv'>
              <Dropdown options={redditPolarityDropDown} value={redditPolarityDefault} placeholder="Select an option" className='dropdownindv' />
            </div>
            <div className='dropdowndiv'>
              <Dropdown options={timeDropDown} value={timeDropDownDefault} placeholder="Select an option" className='dropdownindv' />
            </div>
            <button className='SearchButton' onClick={()=>handleButtonSearch(searchTerm)}>Search</button>
          </div>
          <br/>
          {console.log(dataCollect.length)}
          {dataCollect.length > 0 ? (
          <div>
            {dataCollect.map((result,index) => 
              <div className='reddit_embed' key={result.url}>
                  {/* <iframe
                      id={result.id}
                      src={result.embed_link}
                      sandbox="allow-scripts allow-same-origin allow-popups"
                      style={{border: "none", overflow: "auto" }}
                      height="500"
                      width="1000"
                  ></iframe> */}
                  {console.log(result.url)}
                  <Iframe
                    onInferredClick={() => handleIframeClick(index)}
                    id = {result.url}
                    src={"https://www.redditmedia.com/"+(result.url).substring(23,((result.url).length-1))+"?limit=2/?ref\_source=embed\&amp;ref=share\&amp;embed=true&limit=5"}
                    sandbox="allow-scripts allow-same-origin allow-popups"
                    style={{border: "none", overflow: "auto" }}
                    height = '300px'
                    width="100%"
                  ></Iframe>             
              </div>
              )}
          </div>
           ) : (
          <div>
          <div className='NoResultsDiv'>
            Nothing to display here. Search for a term or click on commonly search terms to see more results.
          </div> 
          <div className='NoResultsImg'>
            <img src = {ProfilePictureCopy} alt="Abhishek" className="about-img" style={{width:"40%",height:"40%"}}></img>
          </div>
          </div>
          )}
        </div>
        <div className="side-box">
            <div>
                Top searched terms
            </div>
            <br/>
            <div className='buttons-start'>
            {items.map((object_ele,i)=>
            <button className='btn-orange' onClick={()=>handleKeywordSearch(object_ele.name)} key={i}>{object_ele.name}</button>
            )}
            </div>
        </div>
    </div>
    </div>
  );
}

export default SearchPage;
