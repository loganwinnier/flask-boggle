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

  const $tbody = $('<tbody>');

  for (let y = 0; y < board.length; y++) {
    const $row = $('<tr>');

    for (let x = 0; x < board.length; x++) {
      const $cell = $(`<td>${board[y][x]}</td>`);

      $row.append($cell);
    }
    $tbody.append($row);
  }
  $table.append($tbody);
}

/** Handle click of go button. gets value from word Input field and responds
 * with error message or adds to played words*/

async function handleGoClick(evt) {
  //Controller Function
  evt.preventDefault();

  $message.empty();

  const word = $wordInput.val().toUpperCase();

  //Seperate Function
  const response = await fetch("/api/score-word", {
    method: "POST",
    body: JSON.stringify({ gameId, word }),
    headers: {
      "content-type": "application/json",
    }
  });

  const { result } = await response.json();

  //Determine where should go function
  if (result === "ok") {

    const $newLi = $("<li>").text(word);
    $playedWords.append($newLi);

  } else {
    $message.text(`${word} is ${result}`);
  }

  //DOM Manipulation

  $form[0].reset();
}

$form.on("submit", handleGoClick);

start();