pragma solidity ^0.4.19;

// Solidity Program to accumulate shares of an enity's debtors balances
// onto an ethereum blockchain.

//The contract is set up by the entity that wants to confirm its balances
//The debtors calculate Shamir shares of their balances off-chain
//and distribute these shares to other receivables who are randomly selected.

//the total of the shares for each receivable is then uploaded and accumulated on the blockchain.

// John McCallig, Nov. 2020
// Licenced under MIT Licences

//contract definition
contract receivablesSum {
    //state variables

    description_struct public description;
    address private owner;

    //structures definitions
    struct description_struct {
        address owner;
        string name;
        string date;
        uint32 assert_balance;
        uint32 sum_balance;
        uint256 prime;
        uint32 shares;
        uint32 min_shares;
    }

    struct receivable {
        bool exists;
        bool uploaded_shares;
    }

    mapping(address => receivable) public receivables_mapping;

    struct point {
        uint256 y;
        uint256 number;
    }

    mapping(uint256 => point) public cum_points;

    //constructor function
    function receivablesSum() public {
        owner = msg.sender;
        description.sum_balance = 0;
    }

    modifier isOwner() {
        require(msg.sender == owner);
        _;
    }

    modifier isReceivable() {
        require(
            receivables_mapping[msg.sender].exists == true,
            "Sender is not a receivable"
        );
        require(
            receivables_mapping[msg.sender].uploaded_shares = true,
            "Receivable has already uploaded shares"
        );
        _;
    }

    //function defintions

    function setDescription(
        string _name,
        string _date,
        uint32 _assert_balance,
        uint256 _prime,
        uint32 _shares,
        uint32 _min_shares
    ) public isOwner {
        description.owner = owner;
        description.name = _name;
        description.date = _date;
        description.assert_balance = _assert_balance;
        description.prime = _prime;
        description.shares = _shares;
        description.min_shares = _min_shares;
    }

    function setReceivables(address[] _addresses) public isOwner {
        for (uint256 i = 0; i < _addresses.length; i++) {
            receivables_mapping[_addresses[i]].exists = true;
            receivables_mapping[_addresses[i]].uploaded_shares = false;
        }
    }

    function checkReceivable(address _address) public view returns (bool) {
        return receivables_mapping[_address].exists;
    }

    function upLoadShares(uint256[] _shares) public isReceivable {
        //shares should be uploaded in threes (x,y,number of shares)
        require(
            description.shares >= 2,
            "Contract description data is not complete"
        );
        require(
            _shares.length % 3 == 0,
            "Shares array is not made up of a multiple of three elements"
        );
        point memory temp_point;
        for (uint256 i = 0; i < _shares.length; i = i + 3) {
            //each share x value should be <= the total number of shares
            require(
                _shares[i] <= description.shares,
                "Share x point is > the number of shares"
            );
            //work out cumulative shares (y) for each point (x) and update cum_points mapping
            temp_point.y = cum_points[_shares[i]].y + _shares[i + 1];
            temp_point.number = cum_points[_shares[i]].number + _shares[i + 2];
            cum_points[_shares[i]] = temp_point;
        }
        // set receivable data to uploaded
        receivables_mapping[msg.sender].uploaded_shares = true;
    }
}
