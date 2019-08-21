using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.CodeAnalysis;

namespace API_Identity.Models.Repository
{
    public interface IUserRepository
    {
        Task<User> Add(User element);
        Task<User> Get(int id);
        Task<IEnumerable<User>> GetAll();
        Task<User> Edit(User element);
        Task<bool> Remove(int id);
        Task<bool> RemoveAll();
        Task<User> GetByEmail(string email);
    }
}