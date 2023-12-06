

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a h)
(on b e)
(ontable c)
(on d a)
(on e i)
(ontable f)
(ontable g)
(on h b)
(ontable i)
(clear c)
(clear d)
(clear f)
(clear g)
)
(:goal
(and
(on b h)
(on c a)
(on e i)
(on f e)
(on g d)
(on i b))
)
)


