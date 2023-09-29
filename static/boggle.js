"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure
  // make main part of board
  const $tbody = $('<tbody>');

  for (let y = 0; y < board.length; y++) {
    const $row = $('<tr>');

    for (let x = 0; x < board.length; x++) {
      const $cell = $(`<td>${board[y][x]}</td>`).attr('id', `c-${y}-${x}`).data("letter", board[y][x]);
      $row.append($cell);
    }
    $tbody.append($row);
  }
  $table.append($tbody);
}

async function handleGoClick(evt){
  evt.preventDefault();

  $message.empty();

  const $wordInput = $("#wordInput");
  const word = $wordInput.value();

  const response = await fetch("/api/score-word",{
      method: "POST",
      body: JSON.stringify({ gameId, word }),
      headers: {
        "content-type": "application/json",
      }
  });

  const { result } = await response.json();

  console.log("result: ", result)

  if(result === "ok"){
    console.log("Ok triggered")
    const $newLi = $("<li>").text(word)
    $playedWords.append($newLi);
  } else {
    $message.text(`${result}`)
  }

}

$("#word-input-btn").on("click", handleGoClick);

start();