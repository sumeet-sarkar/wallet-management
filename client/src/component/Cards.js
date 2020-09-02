import React from 'react';
import './Cards.css'

const cards = props => {
    return(
        <div className="cards" onClick={props.showTransactions}>
            <p>Cards Components {props.id}</p>
            <p>id = {props.id}</p>
            <p>accountNumber = {props.accountNumber}</p>
            <p>bankName = {props.bankName}</p>
            <p>currentBalance = {props.currentBalance}</p>
            <p>email = {props.email}</p>
            <p>phone = {props.phone}</p>
            <p>createdOn = {props.createdOn}</p>
            <p>lastModified = {props.lastModified}</p>
            <p>isDeleted = {props.isDeleted}</p>
        </div>
    )
}

export default cards;