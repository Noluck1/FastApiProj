import logging
from app.shared.dtos.pagination_dto import PaginatedDro
from app.shared.dtos.book_dto import SBooksUpdate, SBooksAdd, SPutBookUpdate
from app.application.i_unit_of_work import IUnitOfWork
from app.application.repositories.i_book_repository import IBookRepository
from app.shared.dtos.book_dto import BooksDto
from app.shared.dtos.auth_dto import UserDto
from app.application.repositories.i_book_access import IBookAccess
from app.application.queries.book_list import BookListFilters, BookListSortBy, SortOrder


logger = logging.getLogger(__name__)

class BookService:
    def __init__(
        self,
        repository: IBookRepository,
        uow: IUnitOfWork,
        book_access: IBookAccess,
    ) -> None:
        self._repository = repository
        self._uow = uow
        self._book_access = book_access


    async def add_book(
            self, 
            book: SBooksAdd,
            current_user: UserDto,
    ) -> BooksDto:
        async with self._uow:
            created_book = await self._repository.add_book(
                book=book,
                author_id=current_user.id
            )
            await self._uow.commit()

            logger.info(
                "Book created: book_id=%s author_id=%s",
                created_book.id,
                current_user.id,
            )

            return created_book

    async def get_books(
        self, 
        page: int, 
        page_size: int,
        filters:BookListFilters,
        sort_by: BookListSortBy,
        sort_order: SortOrder,
    ) -> PaginatedDro[BooksDto]:
        
        async with self._uow:
            books, total = await self._repository.get_books(
                page=page,
                page_size=page_size,
                filters=filters,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        total_pages = (total + page_size - 1) // page_size


        return PaginatedDro[BooksDto](
            item=books,
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )

    async def get_book_id(
            self, 
            book_id: int
    ) -> BooksDto:
        async with self._uow:

            return await self._repository.get_book_id(book_id)

    async def put_update_book(
            self, 
            book_id: int, 
            book: SBooksUpdate,
            current_user: UserDto
    ) -> BooksDto:
        async with self._uow:
            existing_book = await self._repository.get_book_id(
                book_id
            )


            self._book_access.ensure_can_manage(
                user=current_user,
                book=existing_book
            )


            update_book = await self._repository.update_book(
                book_id, 
                book, 
                updated_by_id=current_user.id,
            )
            await self._uow.commit()

            logger.info(
                "Book updated: book_id=%s changed_fields=%s",
                book_id,
                sorted(book.model_fields_set),
            )

            return update_book
        
    async def patch_update_book(
                self, 
                book_id: int, 
                book: SPutBookUpdate,
                current_user: UserDto
        ) -> BooksDto:
            async with self._uow:
                existing_book = await self._repository.get_book_id(
                    book_id
                )
    
    
                self._book_access.ensure_can_manage(
                    user=current_user,
                    book=existing_book
                )
    
    
                update_book = await self._repository.update_book(
                    book_id, 
                    book, 
                    updated_by_id=current_user.id,
                )
                await self._uow.commit()
    
                logger.info(
                    "Book updated: book_id=%s changed_fields=%s",
                    book_id,
                    sorted(book.model_fields_set),
                )
    
                return update_book
    

    async def delete_book(
            self, 
            book_id: int,
            current_user: UserDto,
    ) -> BooksDto:
        async with self._uow:
            existing_book = await self._repository.get_book_id(
                book_id
            )

            self._book_access.ensure_can_manage(
                user=current_user,
                book=existing_book,
            )

            deleted_book_id = await self._repository.delete_book(book_id, updated_by_id=current_user.id)
            await self._uow.commit()

            logger.info(
                "Book deleted: book_id=%s",
                book_id,
            )

            return deleted_book_id