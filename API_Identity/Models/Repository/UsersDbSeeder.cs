using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using API_Identity.Models.Enums;
using API_Identity.Models.Tokens;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace API_Identity.Models.Repository
{
    public class UsersDbSeeder
    {
        private readonly ILogger _logger;

        public UsersDbSeeder(ILoggerFactory loggerFactory)
        {
            _logger = loggerFactory.CreateLogger("UsersDbSeederLogger");
        }

        public async Task SeedAsync(IServiceProvider serviceProvider)
        {
            //Based on EF team's example at https://github.com/aspnet/MusicStore/blob/dev/samples/MusicStore/Models/SampleData.cs
            using (var serviceScope = serviceProvider.GetRequiredService<IServiceScopeFactory>().CreateScope())
            {
                var usersDb = serviceScope.ServiceProvider.GetService<UsersDbContext>();

                if (await usersDb.Database.EnsureCreatedAsync())
                {
                    if (!await usersDb.Users.AnyAsync()) {
                        await InsertDockerSampleData(usersDb);
                    }
                }
            }
        }

        private async Task InsertDockerSampleData(UsersDbContext db)
        {
            var users = GetUsers();
            db.Users.AddRange(users);

            try
            {
                await db.SaveChangesAsync();
            }
            catch (Exception exp)
            {
                _logger.LogError($"Error in {nameof(UsersDbSeeder)}: " + exp.Message);
            }
        }

        private static IEnumerable<User> GetUsers()
        {
            var passwordHasher = new PasswordHasher();
            var result = new List<User>
            {
                new User
                {
                    Email = "test_user@example.com",
                    Phone = "+79991111111",
                    Role = TRole.Admin,
                    PasswordHash = passwordHasher.GenerateIdentityV3Hash("test_user"),
                    FirstName = "test_user",
                    LastName = "test_user"
                }
            };
            return result;
        }
    }
}