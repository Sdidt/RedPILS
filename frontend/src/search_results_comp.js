import Typography from '@mui/material/Typography';
import Slider from '@mui/material/Slider';
import NoResultsImg from "./pic1.png";

const marks = [
  {
    value: -2,
    label: 'LEFT',
  },
  {
    value: 25,
    label: '',
  },
  {
    value: 0,
    label: 'CENTER',
  },
  {
    value: 75,
    label: '',
  },
  {
    value: 2,
    label: 'RIGHT',
  },
];

const SearchResultsComp = (props) => {
    let filterDataCollect = props.data
    let numResults = props.numResults
    return (
    <div>
    {filterDataCollect.length > 0 ? (
        <div>
            <div>
            <Typography variant="h6" gutterBottom style={{color:'white',textAlign:'left'}}>
                Total results returned {numResults} .....
            </Typography>
            <br/>
            </div>
          {filterDataCollect.map((result,index) => 
              <div className='reddit_embed' key={result.url}>
                <iframe
                  id = {result.url}
                  src={"https://www.redditmedia.com/"+(result.url).substring(23,((result.url).length-1))+"?limit=2/?ref\_source=embed\&amp;ref=share\&amp;embed=true&showtitle=%22true%22&theme=dark&limit=0"}
                  sandbox="allow-scripts allow-same-origin allow-popups"
                  style={{border: "none", overflow: "auto" }}
                  height = '300px'
                  width="100%"
                ></iframe>
                <div className="spaceDiv"></div>
                <div className = " progressbarDiv" style={{width:"25%",backgroundColor:"white",padding:"2.2%"}}>
                  <Typography gutterBottom>Prediction class</Typography>
                  <Slider
                    aria-label="Custom marks"
                    defaultValue={[result['political_leaning'],0]}
                    step={0.1}
                    min={-2}
                    max={2}
                    valueLabelDisplay="auto"
                    marks={marks}
                    disabled={true}
                    style={{color:"#ff9301" , width:"90%", height:"20%",'&. MuiSlider-marklabel':{color:"white"}}}
                  />
                </div>
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