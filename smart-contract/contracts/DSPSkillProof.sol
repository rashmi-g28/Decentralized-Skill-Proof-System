// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract DSPSkillProof is Ownable {
    struct Record {
        address user;
        string skill;
        uint16 score; // 0-100
        uint256 timestamp;
    }

    mapping(address => Record[]) private _records;

    event RecordAdded(address indexed user, string skill, uint16 score, uint256 timestamp);

    constructor(address initialOwner) Ownable(initialOwner) {}

    function addRecord(
        address user,
        string calldata skill,
        uint16 score,
        uint256 timestamp
    ) external onlyOwner {
        require(user != address(0), "user is zero address");
        require(bytes(skill).length > 0, "skill empty");
        require(score <= 100, "score out of range");
        _records[user].push(Record({user: user, skill: skill, score: score, timestamp: timestamp}));
        emit RecordAdded(user, skill, score, timestamp);
    }

    function getRecords(address user) external view returns (Record[] memory) {
        return _records[user];
    }

    function getRecordCount(address user) external view returns (uint256) {
        return _records[user].length;
    }
}