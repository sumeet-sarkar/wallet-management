import React, { Component } from 'react';

import Cards from '../component/Cards'
import '../container/Cards.css'

import * as actionTypes from '../store/actions'
import {connect} from 'react-redux'

import axios from 'axios';

class CardsHandler extends Component {

    state = {
        accounts: [],
        transactions: []
    }
    /*
    state = {
        accounts: [
                "id": null,
                "accountNumber": null,
                "bankName": null,
                "currentBalance": null,
                "email": null,
                "phone": null,
                "createdOn": null,
                "lastModified": "2020-08-28T13:00:51.995652+05:30",
                "isDeleted": null
            ]
        }
    }
    */

    componentDidMount = () => {
        axios.get("http://localhost:8000/wallet/")
            .then(response => {
                return response.data
            })
            .then(result => {
                const accounts = []
                result.forEach(res => {
                    accounts.push(res)
                })
                this.props.onAddAccount(accounts)
                //this.setState({accounts:accounts})
            })
            .catch(error => {
                alert(error)
            })
        console.log("component did mount")
    }

    showTransactions = (index) => {
        this.props.setTransactionsWithAccount(index+1)
        this.props.history.push("/transactions")
    }

    testfunc = () => {
        this.state.accounts.map(account => {
            return (
                console.log("haha")
            )
        })
    }

    render() {
        console.log("rendering ", this.props)
        return (
            <div className="cards_handler">
                {this.props.accounts.map((account,index) => {
                    return (
                        <Cards
                            id = {account.id}
                            accountNumber = {account.accountNumber}
                            bankName = {account.bankName}
                            currentBalance = {account.currentBalance}
                            email = {account.email}
                            phone = {account.phone}
                            createdOn = {account.createdOn}
                            lastModified = {account.lastModified}
                            isDeleted = {account.isDeleted}
                            showTransactions = {() => this.showTransactions(index)}
                        />
                    )
                })}
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        accounts: state.accounts
    };
}

const mapDispatchToProps = dispatch => {
    return {
        onAddAccount: (payload) => dispatch({ type: actionTypes.ADD_ACCOUNT, payload: payload }),
        setTransactionsWithAccount: (accountId) => dispatch({ type: actionTypes.SET_TRANSACTIONS_WITH_ACCOUNT, accountId: accountId})
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(CardsHandler);