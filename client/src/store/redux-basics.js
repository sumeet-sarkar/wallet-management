import * as actionTypes from './actions';

const initialState = {
    counter: 10,
    results: [],
    accounts: [],
    transactionsWithAccount: null,
    transactions: []
}

//reducer
const reducer = (state = initialState, action) => {
    switch ( action.type ) {
        case actionTypes.INC_COUNTER:
            return {
                ...state,
                counter: state.counter + 1
            }
        case actionTypes.SET_TRANSACTIONS_WITH_ACCOUNT:
            console.log("twa ", action.accountId)
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
                //accounts: state.accounts.concat(action.payload)
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

/*
//store
const store = createStore(rootReducer);


//subscription
store.subscribe(() => {
    console.log('[Subscription', store.getState())
});

// dispatching action
store.dispatch({type: "INC_COUNTER"});
store.dispatch({type: "ADD_COUNTER", value: 10});
console.log(store.getState());
*/