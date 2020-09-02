import React, { Component } from 'react'
import axios from 'axios'
import * as actionTypes from '../store/actions'
import {connect} from 'react-redux'
import Transactions from '../component/transactions'

class TransactionsHander extends Component{

    state = {
        amount: null
    }

    componentDidMount = () => {
        //const url = "http://localhost:8000/wallet/transactions/?accountid=" + this.props.accountId
        const url = "http://localhost:8000/wallet/transactions/?accountid=1"
        axios.get(url)
            .then(response => {
                return response.data
            })
            .then(result => {
                const transactionsList = []
                result.forEach(res => {
                    transactionsList.push(res)
                })
                this.props.onGetTransactions(transactionsList)
            })
            .catch(error => {
                alert(error)
            })
    }

    editAmount = (event, index) => {
        const url = "http://localhost:8000/wallet/transactions/"
        const body = {
            "id": "28",
            "accountNumber": "1",
            "amountSpent": 20.0,
        }
        axios.put(url, body)
            .then(response => {
                return response.status
            })
            .then(result => (
                //console.log(result)
                this.componentDidMount()
            ))
            .catch(error => {
                alert(error)
            })
    }

    render() {
        console.log("state = ",this.props)
        return(
            <div className="cards_handler">
                {this.props.transactions.map((transaction,index) => {
                    return (
                        <Transactions
                            id = {transaction.id}
                            amountSpent = {transaction.amountSpent}
                            closingBalance = {transaction.closingBalance}
                            reason = {transaction.reason}
                            date = {transaction.date}
                            createdOn = {transaction.createdOn}
                            lastModified = {transaction.lastModified}
                            isDeleted = {transaction.isDeleted}
                            showTransactions = {() => this.showTransactions(index)}
                            editAmount = {(event) => this.editAmount(event,index)}
                        />
                    )
                })}
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        accountId: state.transactionsWithAccount,
        transactions: state.transactions
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onGetTransactions: (transactions) => dispatch({ type: actionTypes.GET_TRANSACTIONS, transactions:transactions })
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(TransactionsHander);