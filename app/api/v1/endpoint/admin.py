from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.model.board import BoardDto
from app.core.dependency import get_current_super_user
from app.service.board_service import BoardService

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    redirect_slashes=False,
    dependencies=[Depends(get_current_super_user)],
)


@router.get("/iam", status_code=status.HTTP_200_OK)
@inject
async def iam():
    return {"status": True}


@router.get("/board/{board_id}", response_model=BoardDto.WithModelBaseInfo, status_code=status.HTTP_200_OK)
@inject
async def get_board(
        board_id: int,
        board_service: BoardService = Depends(Provide[Container.board_service]),
):
    return await board_service.get_by_id(board_id)


@router.post("/board", response_model=BoardDto.WithModelBaseInfo, status_code=status.HTTP_201_CREATED)
@inject
async def create_board(
        upsert_board: BoardDto.Upsert,
        board_service: BoardService = Depends(Provide[Container.board_service]),
):
    return await board_service.add(upsert_board)


@router.patch("/board/{board_id}", response_model=BoardDto.WithModelBaseInfo, status_code=status.HTTP_200_OK)
@inject
async def update_board(
        board_id: int,
        upsert_board: BoardDto.Upsert,
        board_service: BoardService = Depends(Provide[Container.board_service]),
):
    return await board_service.patch(board_id, upsert_board)


@router.delete("/board/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_board(
        board_id: int,
        board_service: BoardService = Depends(Provide[Container.board_service]),
):
    await board_service.remove_by_id(board_id)
