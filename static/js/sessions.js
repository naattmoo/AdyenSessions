const  mySession= JSON.parse(document.getElementById('mySession').innerHTML);
// => { session: 'eyJjaGVja291dH...', id: '123456' }
async function initCheckout() {
	try {
        const configuration = {
            session: {id:mySession.id,sessionData:mySession.sessionData},
            clientKey: "test_ZSIURBAXYREGJLAQY2YZ7CJB2QZEGGFN",
            environment: "test",
             showPayButton: true,
    /**         onSubmit: (state, component) => {
                    makePayment(state.data, window.location.origin).then(response => {
                    console.log(response);
                 if (response.action) {

                        dropin.handleAction(response.action);

                 }else {
                 dropin.setStatus('success');
              dropin.setStatus('success', { message: 'Payment successful!' });
               }})
               .catch(error => {
                 throw Error(error);
               });
              },
              onAdditionalDetails: (state, component) => {
           makeDetailsCall(state.data)
             .then(response => {
               if (response.action) {
                   dropin.handleAction(response.action);
               } else {
                 dropin.setStatus('success');
              dropin.setStatus('success', { message: 'Payment successful!' });
               }
             })
             .catch(error => {
               throw Error(error);
             });
              },**/
            onPaymentCompleted: (result, component) => {
                console.info(result, component);

            },
            onError: (error, component) => {
                console.error(error.name, error.message, error.stack, component);
            },
            paymentMethodsConfiguration: {
           card: { // Example optional configuration for Cards
             enableStoreDetails: true,
             hideCVC: false // Change this to true to hide the CVC field for stored cards
             }
             }
        };
        console.log(configuration);
        const checkout = await AdyenCheckout(configuration);
        //checkout.submitDetails({ details: { redirectResult } });
        const dropin = checkout.create('dropin').mount('#dropin-container');
    } catch (error) {
		console.error(error);
		alert("Error occurred. Look at console for details");
	};
};

initCheckout();
