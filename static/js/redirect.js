console.log(document.getElementById('mySession').innerHTML);
console.log(document.getElementById('redirectResult').innerHTML);
const  mySession= document.getElementById('mySession').innerHTML;
const  redirectResult= document.getElementById('redirectResult').innerHTML;
// => { session: 'eyJjaGVja291dH...', id: '123456' }
async function initCheckout() {
	try {
        const configuration = {
            session: {id:mySession.id,sessionData:mySession.sessionData},
            clientKey: "test_ZSIURBAXYREGJLAQY2YZ7CJB2QZEGGFN",
            environment: "test",
            onPaymentCompleted: (result, component) => {
                console.info(result, component);
                switch (result.resultCode) {
                    case "Authorised":
                    case "Pending":
                    case "Received":
                        window.location.href = "/result/success";
                        break;
                    case "Refused":
                        window.location.href = "/result/failed";
                        break;
                    default:
                        window.location.href = "/result/error";
                        break;
	}
            },
            onError: (error, component) => {
                console.error(error.name, error.message, error.stack, component);
            }
        };
        console.log(configuration);
        const checkout = await AdyenCheckout(configuration);
        checkout.submitDetails({ details: { redirectResult } });
        //const dropin = checkout.create('dropin').mount('#dropin-container');
    } catch (error) {
		console.error(error);
		alert("Error occurred. Look at console for details");
	};
};

initCheckout();