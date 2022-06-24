import logo from './logo.svg';
import './App.css';
import React, {useState} from 'react';
import axios from 'axios';
import {useEffect} from 'react';

const initialFormData = Object.freeze({
  name: '',
  index: 0
});

const initialShownData = Object.freeze({
});



function App() {
  useEffect(()=>{
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const tokenType = urlParams.get('token_type');
    const accessToken = urlParams.get('access_token')
    updateFormData({
      ...formData,
      'token_type': tokenType,
      'access_token': accessToken,
    });
  }, [])
 
  const [formData, updateFormData] = useState(initialFormData);
  const [shownData, updateShownData] = useState(initialShownData);
  const handleChange= (e) =>{
    updateFormData({
      ...formData,
      [e.target.name]: e.target.value.trim()
    });

  }; 
  const handleSearch= (e)=>{
    e.preventDefault();
    console.log(formData);
    const params =new URLSearchParams(formData);
    axios.get(`/api/search?${params}`)
    .then((res)=>{
      const items = JSON.parse(res.data)
      console.log('raw')
      console.log(items)
      console.log(items.data)
      updateShownData(
          items.data
      )
      console.log('hongsun')
      console.log(shownData.items)
      
    });
  };
  const handleRemix= (e) =>{
    const params =new URLSearchParams(formData);
    axios.get(`/api/remix?${params}`)
    .then((res)=>{
      const items = JSON.parse(res.data)
      console.log(items)
    });
  }; 
  

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a href='/api/login'>Login</a>
      <div>
      </div>
        <input type='text' name='name' onChange={handleChange}/>
        <button onClick={handleSearch}>SEARCH</button>
        <Preview items = {shownData} handleRemix={handleRemix}></Preview>
      </header>
    </div>
  );
}

function Preview(props){
  
  console.log('Hello')
  console.log(props.items)
  console.log(props.items.length)
  if ((props && props.items && props.items.length >0) &&  props.items[0].preview_url != null){
    const res = props.items.map((item) => (
      <div>
        <p>Found name: {item.real_name} </p>
        <p>artist: {item.artist} </p>
        <img src ={item.image_url}></img>
        <audio controls src = {item.preview_url}></audio>
        <button onClick={props.handleRemix}>CHOOSE</button>
      </div>
    ));
    return res
   }else{
    return <span></span>
  }
}

export default App;
