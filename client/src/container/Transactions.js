import React, { Component } from 'react'
import axios from 'axios'
import * as actionTypes from '../store/actions'
import {connect} from 'react-redux'
import Rows from '../component/rows'
import Popup from './Popup'

class TransactionsHander extends Component{

    state = {
        showModal: false,
        modal: {
            info: null,
            title: null,
            rows: null,
            actionButtonName: null,
            cancelButtonName: null
        }
    }

    componentDidMount = () => {
        const url = "http://localhost:8000/wallet/transactions/?accountid=" + this.props.accountId
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

    closeModal = () => {
        this.setState({
            showModal: false,
            modal: null
        })
    }

    showModal = (data, action) => {
        this.setState({
            showModal:true,
            modal: { 
                info: data,
                title: `${action} this transaction?`,
                actionButtonName: action,
                cancelButtonName: "Cancel",
                rows: [{
                        inputName: "amountSpent",
                        inputType: "number",
                        inputValue: data.amountSpent,
                    },
                    {
                        inputName: "reason",
                        inputType: "text",
                        inputValue: data.reason,
                    }
                ]
            }
        })
    }

    editTransaction = (data) => {
        const url = "http://localhost:8000/wallet/transactions/"
        const body = {
            "id": data.id,
            "accountNumber": data.accountNumber,
            "amountSpent": parseFloat(data.amountSpent),
            "reason": data.reason
        }
        axios.put(url, body)
            .then(response => {
                return response.status
            })
            .then(() => (
                this.componentDidMount(),
                this.closeModal()
            ))
            .catch(error => {
                alert(error)
                this.closeModal()
            })
    }

    doNothing = () => {
    }

    render() {
        return(
            <div className="cards_handler">
                <Rows
                    columnNames = {["id", "amountSpent", "closingBalance", "reason", "date"]}
                    dataRows = {this.props.transactions}
                    rowClicked = {this.doNothing}
                    performAction = {(data,action) => this.showModal(data, action)}
                />
                {this.state.showModal?
                    <Popup
                        modal = {this.state.modal}
                        cancelButton = {this.closeModal}
                        actionButton = { data => this.editTransaction(data) }
                    />:null
                }
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