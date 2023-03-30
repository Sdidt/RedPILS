import Iframe from 'react-iframe-click';
import NoResultsImg from "./pic1.png";

const SearchResultsComp = (props) => {
    let filterDataCollect = props.data
    console.log(filterDataCollect.length)
    return (
    <div>
    {filterDataCollect.length > 0 ? (
        <div>
          {filterDataCollect.map((result,index) => 
              <div className='reddit_embed' key={result.url}>
                <Iframe
                  id = {result.url}
                  src={"https://www.redditmedia.com/"+(result.url).substring(23,((result.url).length-1))+"?limit=2/?ref\_source=embed\&amp;ref=share\&amp;embed=true&showtitle=%22true%22&theme=dark&limit=5"}
                  sandbox="allow-scripts allow-same-origin allow-popups"
                  style={{border: "none", overflow: "auto" }}
                  height = '300px'
                  width="100%"
                ></Iframe>
            </div>
            )
          }
        </div>
         ) : (
        <div>
        <div className='NoResultsDiv'>
          Nothing to display here. Search for a term or click on commonly search terms to see more results.
        </div> 
        <div className='NoResultsImg'>
          <img src = {NoResultsImg} alt="NoResultImg" className="about-img" style={{width:"40%",height:"40%"}}></img>
        </div>
        </div>
        )
    }
    </div>)
}

export default SearchResultsComp;