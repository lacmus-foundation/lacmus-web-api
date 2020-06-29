using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

namespace Identity.Models.Repository
{
    public class UserRepository : IUserRepository
    {
        private readonly UsersDbContext _context;
        private readonly ILogger _logger;

        public UserRepository(UsersDbContext context, ILoggerFactory loggerFactory)
        {
            _context = context;
            _logger = loggerFactory.CreateLogger("UserRepository");
        }
        public async Task<User> Add(User user)
        {
            if(string.IsNullOrWhiteSpace(user.FirstName))
                throw new InvalidOperationException($"Error in {nameof(Add)}: invalid first name");
            if(string.IsNullOrWhiteSpace(user.FirstName))
                throw new InvalidOperationException($"Error in {nameof(Add)}: invalid last name");
            if(string.IsNullOrWhiteSpace(user.Phone))
                throw new InvalidOperationException($"Error in {nameof(Add)}: invalid phone");
            /* TODO: add phone number check https://github.com/twcclegg/libphonenumber-csharp/blob/master
             * TODO: add last and first name check with regexp */
            
            _context.Add(user);
            try
            {
                await _context.SaveChangesAsync();
            }
            catch (Exception exp)
            {
                _logger.LogError($"Error in {nameof(Add)}: " + exp.Message);
            }

            return user;
        }

        public async Task<User> Get(int id)
        {
            return await _context.Users.SingleOrDefaultAsync(u => u.Id == id);
        }

        public async Task<IEnumerable<User>> GetAll()
        {
            return await _context.Users.OrderBy(u => u.LastName).ToListAsync();
        }

        public async Task<User> Edit(User user)
        {
            _context.Users.Attach(user);
            _context.Entry(user).State = EntityState.Modified;
            try
            {
                return await _context.SaveChangesAsync() > 0 ? user : null;
            }
            catch (Exception exp)
            {
                _logger.LogError($"Error in {nameof(Edit)}: " + exp.Message);
            }
            return null;
        }

        public async Task<bool> Remove(int id)
        {
            var user = await _context.Users.SingleOrDefaultAsync(c => c.Id == id);
            _context.Remove(user);
            try
            {
                return await _context.SaveChangesAsync() > 0;
            }
            catch (Exception exp)
            {
                _logger.LogError($"Error in {nameof(Remove)}: " + exp.Message);
            }
            return false;
        }

        public async Task<bool> RemoveAll()
        {
            _context.Users.RemoveRange(await GetAll());
            try
            {
                return await _context.SaveChangesAsync() > 0;
            }
            catch (Exception exp)
            {
                _logger.LogError($"Error in {nameof(Remove)}: " + exp.Message);
            }
            return false;
        }

        public async Task<User> GetByEmail(string email)
        {
            return await _context.Users.SingleOrDefaultAsync(u => u.Email == email);
        }
    }
}