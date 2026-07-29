import sys

def get_wallet_emulation_script():

    return """

window.__wallet_requests__ = [];

window.ethereum = {

    isMetaMask: true,

    selectedAddress:
        "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",

    chainId: "0x1",

    networkVersion: "1",

    providers: [

        {
            isMetaMask: true
        },

        {
            isCoinbaseWallet: true
        },

        {
            isRabby: true
        }

    ],

    request: async function(args){

        window.__wallet_requests__.push(args);

        const method = args.method;

        if(method === "eth_accounts"){

            return [

                "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"

            ];

        }

        if(method === "eth_requestAccounts"){

            return [

                "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"

            ];

        }

        if(method === "eth_chainId"){

            return "0x1";

        }

        if(method === "eth_getBalance"){

            return "0x3635C9ADC5DEA00000";

        }

        if(method === "wallet_switchEthereumChain"){

            return null;

        }

        if(

            method === "personal_sign" ||

            method === "eth_signTypedData"

        ){

            return "SIGNATURE_CAPTURED";

        }

        return null;

    }

};

"""