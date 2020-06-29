using Microsoft.EntityFrameworkCore;

namespace Identity.Models.Repository
{
    public class UsersDbContext : DbContext
    {
        public DbSet<User> Users { get; set; }

        public UsersDbContext (DbContextOptions<UsersDbContext> options) : base(options) { }
    }
}