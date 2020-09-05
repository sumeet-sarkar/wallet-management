import React from 'react';
import './App.css';
import Header from './container/Header';
import Accounts from './container/Accounts';
import {BrowserRouter, Route} from 'react-router-dom';
import Transactions from './container/Transactions';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Route path="/" component={Header}/>
        <Route path="/" exact component={Accounts}/>
        <Route path="/transactions" exact component={Transactions}/>
      </div>
    </BrowserRouter>
  );
}

export default App;