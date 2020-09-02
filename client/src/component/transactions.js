import React from 'react';
import './Cards.css'

const transactions = props => {
    return(
        <div className="cards">
            <p>Transactions {props.id}</p>
            <p>id = {props.id}</p>
            <p>closingBalance = {props.closingBalance}</p>
            <p>amountSpent = {props.amountSpent}</p>
            <p>reason = {props.reason}</p>
            <p>date = {props.date}</p>
            <p>createdOn = {props.createdOn}</p>
            <p>lastModified = {props.lastModified}</p>
            <button onClick={props.editAmount}>
                Edit
            </button>
        </div>
    )
}

export default transactions;