import * as actionTypes from './actions';

const initialState = {
    counter: 10,
    results: [],
    accounts: [],
    transactionsWithAccount: null,
    transactions: []
}

const reducer = (state = initialState, action) => {
    switch ( action.type ) {
        case actionTypes.INC_COUNTER:
            return {
                ...state,
                counter: state.counter + 1
            }
        case actionTypes.SET_TRANSACTIONS_WITH_ACCOUNT:
            return {
                ...state,
                transactionsWithAccount: action.accountId
            }
        case actionTypes.ADD_ARRAY:
            return {
                ...state,
                results: state.results.concat(state.counter)
            }
        case actionTypes.DEL_ARRAY:
            const updatedArray = state.results.filter(result => result.id !== action.resultElId);
            return {
                ...state,
                results: updatedArray
            }
        case actionTypes.ADD_ACCOUNT:
            const updatedAccounts = []
            action.payload.forEach(account => {
                updatedAccounts.push(account)
            })
            return {
                ...state,
                accounts: updatedAccounts
            }
        case actionTypes.GET_TRANSACTIONS:
            const transactions = []
            action.transactions.forEach(transaction => {
                transactions.push(transaction)
            })
            return {
                ...state,
                transactions: transactions
            }
        default:
            return state;
    }
}

export default reducer;
