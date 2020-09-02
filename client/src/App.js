import React from 'react';
import logo from './logo.svg';
import './App.css';
import Header from './container/Header';
import Cards from './container/Cards';
import {BrowserRouter, Route} from 'react-router-dom';
import Transactions from './container/Transactions';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Route path="/" component={Header}/>
        <Route path="/" exact component={Cards}/>
        <Route path="/transactions" exact component={Transactions}/>
      </div>
    </BrowserRouter>
  );
}

export default App;